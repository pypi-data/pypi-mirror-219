from prolog_primitives.basic import DistributedElements
from typing import Generator
from prolog_primitives.basic import Utils
from ..collections import SharedCollections
from .transformationClass import Pipeline
from datasets import Dataset

class __Transform(DistributedElements.DistributedPrimitive):
    
    def solve(self, request: DistributedElements.DistributedRequest) -> Generator[DistributedElements.DistributedResponse, None, None]:
        dataset_in_ref = request.arguments[0]
        transf_ref = request.arguments[1]
        dataset_out_ref = request.arguments[2]
        
        if(not transf_ref.HasField('var')):
            transf: Pipeline = SharedCollections().getPipeline(Utils.parseArgumentMsg(transf_ref))
            
            if(not dataset_in_ref.HasField("var") and dataset_out_ref.HasField("var")):
                dataset_in: Dataset = SharedCollections().getDataset(Utils.parseArgumentMsg(dataset_in_ref))
                schemaId = SharedCollections().addSchema(transf.computeFinalSchema())
                dataset_out = transf.apply(dataset_in)
                id = SharedCollections().addDataset(dataset_out, schemaId)

                yield request.replySuccess(substitutions={
                    dataset_out_ref.var: Utils.buildConstantArgumentMsg(id)
                    }, hasNext=False)
            elif(dataset_in_ref.HasField("var") and not dataset_out_ref.HasField("var")):
                dataset_out: Dataset = SharedCollections().getDataset(Utils.parseArgumentMsg(dataset_out_ref))
                dataset_in: Dataset = transf.invert(dataset_out)
                id = SharedCollections().addDataset(dataset_in, transf.originalSchema)

                yield request.replySuccess(substitutions={
                    dataset_in_ref.var: Utils.buildConstantArgumentMsg(id)
                    }, hasNext=False)
        else:
            yield request.replyFail()
            
            
transformPrimitive = DistributedElements.DistributedPrimitiveWrapper("transform", 3, __Transform())