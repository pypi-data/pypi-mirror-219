from prolog_primitives.basic import DistributedElements
from typing import Generator
from prolog_primitives.basic import Utils
from ..collections import SharedCollections
import tensorflow as tf
from datasets import Dataset

class __InputLayer(DistributedElements.DistributedPrimitive):
    
    def solve(self, request: DistributedElements.DistributedRequest) -> Generator[DistributedElements.DistributedResponse, None, None]:
        size = request.arguments[0]
        topology_ref = request.arguments[1]
        
        if(not size.HasField('var') and topology_ref.HasField('var')):
            size = int(Utils.parseArgumentMsg(size))
            id = SharedCollections().addTopology([tf.keras.Input(shape=(size,), name="input")])
            yield request.replySuccess(substitutions={
                topology_ref.var: Utils.buildConstantArgumentMsg(id)
                }, hasNext=False)
        else:
            yield request.replyFail()
            
            
inputLayerPrimitive = DistributedElements.DistributedPrimitiveWrapper("input_layer", 2, __InputLayer())