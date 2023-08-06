from prolog_primitives.basic import DistributedElements
from typing import Generator
from prolog_primitives.basic import Utils
from ..collections import SharedCollections
from .transformationClass import Dropper, Pipeline

class __Drop(DistributedElements.DistributedPrimitive):
    
    def solve(self, request: DistributedElements.DistributedRequest) -> Generator[DistributedElements.DistributedResponse, None, None]:
        transf_in_ref = request.arguments[0]
        attributes = request.arguments[1]
        transf_out_ref = request.arguments[2]
        
        if(not transf_in_ref.HasField('var') and not attributes.HasField('var') and transf_out_ref.HasField('var')):
            transf_in_id = Utils.parseArgumentMsg(transf_in_ref)
            transf: Pipeline = SharedCollections().getPipeline(transf_in_id)
            listOfAttr = Utils.parseArgumentMsgList(attributes)
            if(listOfAttr != []):
                attributes = listOfAttr
            else:
                attributes = [Utils.parseArgumentMsg(attributes)]
                
            id = SharedCollections().addPipeline(transf.append(dict.fromkeys(attributes, [Dropper()])))
            yield request.replySuccess(substitutions={
                transf_out_ref.var: Utils.buildConstantArgumentMsg(id)
                }, hasNext=False)
        else:
            yield request.replyFail()
            
            
dropPrimitive = DistributedElements.DistributedPrimitiveWrapper("drop", 3, __Drop())