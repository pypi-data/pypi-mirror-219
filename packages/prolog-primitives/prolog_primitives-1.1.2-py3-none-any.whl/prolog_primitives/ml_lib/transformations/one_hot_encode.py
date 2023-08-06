from prolog_primitives.basic import DistributedElements
from typing import Generator
from prolog_primitives.basic import Utils
from ..collections import SharedCollections
from ..schema.schemaClass import Schema
from .transformationClass import OneHotEncoder, Pipeline

class __One_Hot_Encode(DistributedElements.DistributedPrimitive):
    
    def solve(self, request: DistributedElements.DistributedRequest) -> Generator[DistributedElements.DistributedResponse, None, None]:
        transf_in_ref = request.arguments[0]
        attributes = request.arguments[1]
        transf_out_ref = request.arguments[2]
        
        if(not transf_in_ref.HasField('var') and not attributes.HasField('var') and transf_out_ref.HasField('var')):
            transf: Pipeline = SharedCollections().getPipeline(Utils.parseArgumentMsg(transf_in_ref))
            schema: Schema = SharedCollections().getSchema(transf.originalSchemaId)
            listOfAttr = Utils.parseArgumentMsgList(attributes)
            if(listOfAttr != []):
                attributes = listOfAttr
            else:
                attributes = [Utils.parseArgumentMsg(attributes)]
            
            layers = {}
            for attr in attributes:
                vocab = list(filter(lambda x: x.name == attr ,schema.attributes)).pop().vocab
                layers[attr] = [OneHotEncoder(vocab)]
            
            id = SharedCollections().addPipeline(transf.append(layers))
            yield request.replySuccess(substitutions={
                transf_out_ref.var: Utils.buildConstantArgumentMsg(id)
                }, hasNext=False)
        else:
            yield request.replyFail()
            
            
one_hot_encodePrimitive = DistributedElements.DistributedPrimitiveWrapper("one_hot_encode", 3, __One_Hot_Encode())