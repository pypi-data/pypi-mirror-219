from prolog_primitives.basic import DistributedElements
from typing import Generator
from prolog_primitives.basic import Utils
from ..collections import SharedCollections
from .transformationClass import Pipeline

class __SchemaTrasformation(DistributedElements.DistributedPrimitive):
    
    def solve(self, request: DistributedElements.DistributedRequest) -> Generator[DistributedElements.DistributedResponse, None, None]:
        schema_ref = request.arguments[0]
        transf_ref = request.arguments[1]
        
        if(not schema_ref.HasField('var') and transf_ref.HasField('var')):
            schema_id = Utils.parseArgumentMsg(schema_ref)
            pipeline = Pipeline(schema_id)
            id = SharedCollections().addPipeline(pipeline)
            yield request.replySuccess(substitutions={
                transf_ref.var: Utils.buildConstantArgumentMsg(id)
                }, hasNext=False)
        elif(schema_ref.HasField('var') and not transf_ref.HasField('var')):
            transformation_id = Utils.parseArgumentMsg(transf_ref)
            transformation: Pipeline = SharedCollections().getPipeline(transformation_id)
            id = SharedCollections().addSchema(transformation.computeFinalSchema())
            yield request.replySuccess(substitutions = {
                schema_ref.var: Utils.buildConstantArgumentMsg(id)
            }, hasNext=False)            
        else:
            yield request.replyFail()
            
            
schemaTrasformation = DistributedElements.DistributedPrimitiveWrapper("schema_transformation", 2, __SchemaTrasformation())