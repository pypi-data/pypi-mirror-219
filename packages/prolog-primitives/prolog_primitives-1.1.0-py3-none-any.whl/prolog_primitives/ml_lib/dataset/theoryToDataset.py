from prolog_primitives.basic import DistributedElements
from prolog_primitives.generatedProto import primitiveService_pb2 as primitiveMsg
from prolog_primitives.generatedProto import basicMessages_pb2 as basicMsg
from prolog_primitives.generatedProto import errorsMessages_pb2 as errorMsg
from typing import Generator
from prolog_primitives.basic import Utils
from ..collections import SharedCollections
from datasets import Dataset

class __TheoryToDatasetPrimitive(DistributedElements.DistributedPrimitive):
    
    def solve(self, request: DistributedElements.DistributedRequest) -> Generator[DistributedElements.DistributedResponse, None, None]:
        schema_name = request.arguments[0]
        dataset_ref = request.arguments[1]
        if(not schema_name.HasField("var") and dataset_ref.HasField("var")):
            schemaId = str(Utils.parseArgumentMsg(next(request.subSolve(
                query = basicMsg.StructMsg(functor="theory_to_schema", arguments=[basicMsg.ArgumentMsg(var="X")]))
                 ).substitutions["X"]))         
            schema = SharedCollections().getSchema(schemaId)
            
            data = dict(list(map(lambda x: (x.name,[]), schema.attributes)))
            for i in request.inspectKb(
                primitiveMsg.InspectKbMsg.STATIC,
                [(primitiveMsg.InspectKbMsg.STARTS_WITH, str(Utils.parseArgumentMsg(schema_name)))]):    
                if(i == None and len(data) == 0):
                    yield request.replyFail()
                elif(i != None):
                    i = Utils.parseStructMsg(i.arguments[0].struct)
                    for j in zip(schema.attributes, i.arguments):
                        value = j[0].typeCastElement(str(j[1]))
                        if(value == None):
                            yield request.replyError(primitiveMsg.ErrorMsg(
                                message = "One of " + j[0].name + " was not the correct type",
                                context=request.context,
                                resolutionException = errorMsg.ResolutionExceptionMsg()
                            ))
                            raise Exception("Wrong typecasting in attributes")
                        else:
                            data[j[0].name].append(value)
            
            dataset = Dataset.from_dict(data).with_format("tf")
            datasetId = SharedCollections().addDataset(dataset, schemaId)
            yield request.replySuccess(substitutions={
                dataset_ref.var: Utils.buildConstantArgumentMsg(datasetId)
                }, hasNext=False)
        else:
            yield request.replyFail()
            
            
theoryToDatasetPrimitive = DistributedElements.DistributedPrimitiveWrapper("theory_to_dataset", 2, __TheoryToDatasetPrimitive())