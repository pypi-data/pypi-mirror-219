from prolog_primitives.basic import DistributedElements
from typing import Generator
from prolog_primitives.basic import Utils
from ..collections import SharedCollections
from .transformationClass import  Pipeline
from datasets import Dataset

class __Fit(DistributedElements.DistributedPrimitive):
    
    def solve(self, request: DistributedElements.DistributedRequest) -> Generator[DistributedElements.DistributedResponse, None, None]:
        transf_in_ref = request.arguments[0]
        dataset_ref = request.arguments[1]
        transf_out_ref = request.arguments[2]
        
        if(not transf_in_ref.HasField('var') and not dataset_ref.HasField('var') and transf_out_ref.HasField('var')):
            transf: Pipeline = SharedCollections().getPipeline(Utils.parseArgumentMsg(transf_in_ref))
            dataset: Dataset = SharedCollections().getDataset(Utils.parseArgumentMsg(dataset_ref))
            id = SharedCollections().addPipeline(transf.adapt(dataset))
            yield request.replySuccess(substitutions={
                transf_out_ref.var: Utils.buildConstantArgumentMsg(id)
                }, hasNext=False)
        else:
            yield request.replyFail()
            
            
fitPrimitive = DistributedElements.DistributedPrimitiveWrapper("fit", 3, __Fit())