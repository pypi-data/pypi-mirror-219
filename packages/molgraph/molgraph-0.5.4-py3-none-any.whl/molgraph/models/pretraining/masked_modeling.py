import tensorflow as tf

import keras
from keras import layers

from typing import Optional
from typing import List

from molgraph.tensors.graph_tensor import GraphTensor

from molgraph.layers.preprocessing.masking import FeatureMasking
from molgraph.layers.preprocessing.embedding_lookup import EmbeddingLookup
from molgraph.layers.postprocessing.gather_incident import GatherIncident


class MaskedGraphModeling(keras.Model):
    
    '''Masked Graph Modeling (MGM) inspired by Masked Language Modeling (MLM).
    
    See e.g. Hu et al. [#]_ and Devlin et al. [#]_.
    
    The encoder part of the MGM model is the model to be finetuned
    for downstream modeling. In this MGM model, masking layer(s) 
    will be prepended to randomly mask out node and/or edge features 
    of a certain rate. Furthermore, a classification layer is appended 
    to the encoder to produce multi-class predictions; with the objective 
    to predict the masked node and/or edge features. 
    
    Currently, this MGM model only support Tokenized molecular graphs
    which have been embedded via `EmbeddingLookup`. A Featurized molecular 
    graph (without `EmbeddingLookup`) is less straight forward to implement, 
    though it could be implemented by e.g. creating random vectors for each 
    masked node/edge.
    
    Args:
        encoder (tf.keras.Model):
            The model to be pretrained and used for downstream tasks. The 
            first layer(s) of the model should embed (via `EmbeddingLookup`) 
            (later on, possibly masked) node/edge embeddings from tokenized 
            molecular graphs (obtain via `Tokenizer`).
        node_feature_decoder (None, tf.keras.layers.Layer):
            Optionally supply a decoder which turns the node embeddings 
            into a softmaxed prediction. If None, a linear transdformation
            followed by a softmax activation will be used. Default to None.
        edge_feature_decoder (None, tf.keras.layers.Layer):
            Optionally supply a decoder which turns the edge embeddings 
            into a softmaxed prediction. If None, a linear transdformation
            followed by a softmax activation will be used. Default to None.
        node_feature_masking_rate (None, float):
            The rate at which node features should be masked. If None, or
            0.0, no masking will be performed on the node features. Default
            to 0.15.
        edge_feature_masking_rate (None, float):
            The rate at which edge features should be masked. If None, or
            0.0, no masking will be performed on the edge features. Default
            to 0.15.
    
    References:
        .. [#] https://arxiv.org/pdf/1905.12265.pdf
        .. [#] https://arxiv.org/pdf/1810.04805.pdf
    '''
    
    def __init__(
        self, 
        encoder: keras.Model, 
        node_feature_decoder: Optional[layers.Layer] = None,
        edge_feature_decoder: Optional[layers.Layer] = None,
        node_feature_masking_rate: Optional[float] = 0.15,
        edge_feature_masking_rate: Optional[float] = 0.15,
        name: Optional[str] = 'MaskedGraphModeling',
        **kwargs,
    ):
        super().__init__(name=name, **kwargs)
        
        self.encoder = encoder

        self.node_feature_masking_rate = node_feature_masking_rate or 0.0
        self.edge_feature_masking_rate = edge_feature_masking_rate or 0.0

        self.node_feature_decoder = node_feature_decoder
        self.edge_feature_decoder = edge_feature_decoder

        for layer in self.encoder.layers:
            
            if isinstance(layer, EmbeddingLookup):
                # feature_type is either "node" or "edge"
                feature_type: str = layer.feature
                
                if (
                    feature_type == 'node_feature' and 
                    node_feature_masking_rate > 0.0
                ):
                    self.node_feature_masking_layer = FeatureMasking(
                        feature=feature_type, 
                        rate=self.node_feature_masking_rate, 
                        mask_token=layer.mask_token)
                    
                    self.lookup_node_feature_label = layer.lookup_table.lookup

                    if self.node_feature_decoder is None:
                        self.node_feature_decoder = layers.Dense(
                            units=layer.vocabulary_size()-1, 
                            activation='softmax')
                        
                elif (
                    feature_type == 'edge_feature' and 
                    edge_feature_masking_rate > 0.0
                ):
                    self.edge_feature_masking_layer = FeatureMasking(
                        feature=feature_type, 
                        rate=self.edge_feature_masking_rate, 
                        mask_token=layer.mask_token)
                                    
                    self.lookup_edge_feature_label = layer.lookup_table.lookup

                    if self.edge_feature_decoder is None:
                        self.edge_feature_decoder = layers.Dense(
                            units=layer.vocabulary_size()-1, 
                            activation='softmax')
                        
                    self.gather_incident = GatherIncident()
            
    def call(
        self, 
        tensor: GraphTensor, 
        training: Optional[bool] = None
    ) -> GraphTensor:
        return self.encoder(tensor, training=training)
    
    def train_step(self, tensor: GraphTensor) -> dict:
        
        with tf.GradientTape() as tape:

            tensor = self._call(tensor, training=True)

            loss = 0.0

            if self.node_feature_masking_rate > 0.0:
                node_loss, (node_true, node_pred) = self._compute_node_loss(
                    tensor)
                loss += node_loss

            if self.edge_feature_masking_rate > 0.0:
                edge_loss, (edge_true, edge_pred) = self._compute_edge_loss(
                    tensor)
                loss += edge_loss

        variables = self.trainable_variables
        gradients = tape.gradient(loss, variables)
        self.optimizer.apply_gradients(zip(gradients, variables))

        if self.node_feature_masking_rate > 0.0:
            self.node_loss_tracker.update_state(node_loss)
            for metric in self.node_metrics:
                metric.update_state(node_true, node_pred)

        if self.edge_feature_masking_rate > 0.0:
            self.edge_loss_tracker.update_state(edge_loss)
            for metric in self.edge_metrics:
                metric.update_state(edge_true, edge_pred)

        return {metric.name: metric.result() for metric in self.metrics}
    
    def test_step(self, tensor: GraphTensor) -> dict:

        tensor = self._call(tensor, training=False)

        if self.node_feature_masking_rate > 0.0:
            node_loss, (node_true, node_pred) = self._compute_node_loss(
                tensor)

        if self.edge_feature_masking_rate > 0.0:
            edge_loss, (edge_true, edge_pred) = self._compute_edge_loss(
                tensor)
            
        if self.node_feature_masking_rate > 0.0:
            self.node_loss_tracker.update_state(node_loss)
            for metric in self.node_metrics:
                metric.update_state(node_true, node_pred)

        if self.edge_feature_masking_rate > 0.0:
            self.edge_loss_tracker.update_state(edge_loss)
            for metric in self.edge_metrics:
                metric.update_state(edge_true, edge_pred)

        return {metric.name: metric.result() for metric in self.metrics}
       
    def predict_step(self, tensor: GraphTensor) -> GraphTensor:
        return self(tensor, training=False)

    def compile(
        self, 
        optimizer: keras.optimizers.Optimizer, 
        loss: Optional[keras.losses.Loss] = None, 
        metrics: Optional[List[keras.metrics.Metric]] = None, 
        node_feature_loss_weight: Optional[float] = None,
        edge_feature_loss_weight: Optional[float] = None, 
        *args, 
        **kwargs
    ):
        super().compile(
            optimizer=optimizer, 
            loss=None, 
            metrics=None, 
            *args, 
            **kwargs)

        self.loss_fn = (
            keras.losses.SparseCategoricalCrossentropy() if loss is None else 
            loss)
   
        metrics = [] if metrics is None else metrics

        if self.node_feature_masking_rate > 0.0:
            self.node_metrics = []
            self._node_feature_loss_weight = (
                node_feature_loss_weight or 1.0)
            self.node_loss_tracker = keras.metrics.Mean(
                name='node_' + self.loss_fn.name)
            for metric in metrics:
                metric_config = metric.get_config()
                metric_config['name'] = 'node_' + metric_config['name']
                self.node_metrics.append(metric.from_config(metric_config))

        if self.edge_feature_masking_rate > 0.0:
            self.edge_metrics = []
            self._edge_feature_loss_weight = (
                edge_feature_loss_weight or 1.0)
            self.edge_loss_tracker = keras.metrics.Mean(
                name='edge_' + self.loss_fn.name)
            for metric in metrics:
                metric_config = metric.get_config()
                metric_config['name'] = 'edge_' + metric_config['name']
                self.edge_metrics.append(metric.from_config(metric_config))

    @property
    def metrics(self) -> List[keras.metrics.Metric]:
        metrics = []
        if self.node_feature_masking_rate > 0.0:
            metrics.append(self.node_loss_tracker)
        if self.edge_feature_masking_rate > 0.0:
            metrics.append(self.edge_loss_tracker)
        return metrics + self.node_metrics + self.edge_metrics
    
    def get_config(self) -> dict:
        config = super().get_config()
        config.update({
            'encoder': layers.serialize(self.encoder),
            'node_feature_decoder': layers.serialize(self.decoder['node']),
            'edge_feature_decoder': layers.serialize(self.decoder['edge']),
            'node_masking_rate': self.masking_rate['node'],
            'edge_masking_rate': self.masking_rate['edge'],
        })
        return config
    
    def _call(
        self, 
        tensor: GraphTensor,
        training: Optional[bool] = None,    
    ) -> GraphTensor:
        
        if isinstance(tensor.node_feature, tf.RaggedTensor):
            tensor = tensor.merge()
        
        new_data = {}

        if self.node_feature_masking_rate > 0.0:
            node_feature = tensor.node_feature
            tensor = self.node_feature_masking_layer(tensor)
            mask_token = self.node_feature_masking_layer.mask_token
            node_feature_mask = tf.where(
                tensor.node_feature == mask_token, True, False)
            new_data['node_feature_mask'] = node_feature_mask 
            new_data['node_feature_label'] = self.lookup_node_feature_label(
                node_feature) - 1
        
        if self.edge_feature_masking_rate > 0.0:
            edge_feature = tensor.edge_feature
            tensor = self.edge_feature_masking_layer(tensor)
            mask_token = self.edge_feature_masking_layer.mask_token
            edge_feature_mask = tf.where(
                tensor.edge_feature == mask_token, True, False)
            new_data['edge_feature_mask'] = edge_feature_mask 
            new_data['edge_feature_label'] = self.lookup_edge_feature_label(
                edge_feature) - 1
        
        tensor = tensor.update(new_data)

        return self(tensor, training=training)
    
    def _compute_node_loss(
        self, 
        tensor: GraphTensor
    ) -> float:
        y_pred = self._predict_node_features(tensor)
        y_true = tf.boolean_mask(
            tensor.node_feature_label, tensor.node_feature_mask)
        loss = self.loss_fn(y_true, y_pred) * self._node_feature_loss_weight
        return loss, (y_true, y_pred)
    
    def _compute_edge_loss(
        self, 
        tensor: GraphTensor
    ) -> float:
        y_pred = self._predict_edge_features(tensor)
        y_true = tf.boolean_mask(
            tensor.edge_feature_label, tensor.edge_feature_mask)
        loss = self.loss_fn(y_true, y_pred) * self._edge_feature_loss_weight
        return loss, (y_true, y_pred)
    
    def _predict_node_features(
        self, 
        tensor: GraphTensor
    ) -> tf.Tensor:
        node_feature = tf.boolean_mask(
            tensor.node_feature, tensor.node_feature_mask)
        y_pred = self.node_feature_decoder(node_feature)
        return y_pred

    def _predict_edge_features(
        self, 
        tensor: GraphTensor
    ) -> tf.Tensor:
        tensor = tf.boolean_mask(
            tensor, tensor.edge_feature_mask, axis='edge')
        edge_feature = self.gather_incident(tensor)
        y_pred = self.edge_feature_decoder(edge_feature)
        return y_pred