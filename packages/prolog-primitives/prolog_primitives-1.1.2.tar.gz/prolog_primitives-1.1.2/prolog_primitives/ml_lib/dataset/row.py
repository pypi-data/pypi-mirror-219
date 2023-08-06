from prolog_primitives.basic import DistributedElements
from typing import Generator
from prolog_primitives.basic import Utils
from ..collections import SharedCollections
import tensorflow as tf

class __RowPrimitive(DistributedElements.DistributedPrimitive):
    
    def solve(self, request: DistributedElements.DistributedRequest) -> Generator[DistributedElements.DistributedResponse, None, None]:
        dataset_ref = request.arguments[0]
        index = request.arguments[1]
        values = request.arguments[2]
        
        def getRow(i): 
            return list(map(
                    Utils.stringsConverter,
                    [tf.get_static_value(x) for x in dataset[i].values()]))
        
        if(not dataset_ref.HasField("var") and values.HasField("var")):
            dataset = SharedCollections().getDataset(str(Utils.parseArgumentMsg(dataset_ref)))
                
            if(not index.HasField("var")):
                i = int(Utils.parseArgumentMsg(index))
                yield request.replySuccess({
                    values.var: Utils.fromListToArgumentMsg(getRow(i))
                }, hasNext=False)
            else:
                i = 0
                while(i < dataset.shape[0]):
                    row = getRow(i)
                    i += 1
                    yield request.replySuccess(
                        substitutions={
                            index.var: Utils.buildConstantArgumentMsg(i),
                            values.var: Utils.fromListToArgumentMsg(row)
                            }, hasNext = (i < dataset.shape[0]))
        else:
            yield request.replyFail()
            
            
rowPrimitive = DistributedElements.DistributedPrimitiveWrapper("row", 3, __RowPrimitive())