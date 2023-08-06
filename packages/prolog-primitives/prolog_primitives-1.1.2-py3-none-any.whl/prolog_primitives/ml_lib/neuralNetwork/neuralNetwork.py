from prolog_primitives.basic import DistributedElements
from typing import Generator
from prolog_primitives.basic import Utils
from ..collections import SharedCollections
import tensorflow as tf
from datasets import Dataset

class __NeuralNetwork(DistributedElements.DistributedPrimitive):
    
    def solve(self, request: DistributedElements.DistributedRequest) -> Generator[DistributedElements.DistributedResponse, None, None]:
        topology_ref = request.arguments[0]
        predictor_ref = request.arguments[1]
        
        if(not topology_ref.HasField('var') and predictor_ref.HasField('var')):
            topology = SharedCollections().getTopology(Utils.parseArgumentMsg(topology_ref))
            
            output = topology[0]
            for i in topology[1:]:
                output = i(output)
            
            model = tf.keras.Model(
                inputs=[topology[0]], outputs = [output]
            )
            
            id = SharedCollections().addModel(model)
            yield request.replySuccess(substitutions={
                predictor_ref.var: Utils.buildConstantArgumentMsg(id)
                }, hasNext=False)
        else:
            yield request.replyFail()
            
            
neuralNetworkPrimitive = DistributedElements.DistributedPrimitiveWrapper("neural_network", 2, __NeuralNetwork())