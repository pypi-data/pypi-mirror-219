from prolog_primitives.basic import DistributedElements
from prolog_primitives.generatedProto.sideEffectsMessages_pb2 import SetClausesOfKBMsg, SideEffectMsg
import prolog_primitives.generatedProto.basicMessages_pb2 as basicMsg
from typing import Generator
from prolog_primitives.basic import Utils
from ..collections import SharedCollections
import tensorflow as tf

def wrapInClause(struct: basicMsg.StructMsg):
    finalStruct = basicMsg.StructMsg(
        functor = ":-"
    )
    finalStruct.arguments.append(Utils.buildConstantArgumentMsg(struct))
    finalStruct.arguments.append(Utils.buildConstantArgumentMsg(True))
    return finalStruct

class __TheoryFromDatasetPrimitive(DistributedElements.DistributedPrimitive):
    
    def solve(self, request: DistributedElements.DistributedRequest) -> Generator[DistributedElements.DistributedResponse, None, None]:
        schema_ref = request.arguments[0]
        dataset_ref = request.arguments[1]
        if(not schema_ref.HasField("var") and not dataset_ref.HasField("var")):  
            schema = SharedCollections().getSchema(Utils.parseArgumentMsg(schema_ref))
            dataset = SharedCollections().getDataset(Utils.parseArgumentMsg(dataset_ref))
            
            clauses = []
            clauses.append(wrapInClause(
                basicMsg.StructMsg(
                    functor="schema_name",
                    arguments=[Utils.buildConstantArgumentMsg(schema.name)]
            )))
            clauses.append(wrapInClause(
                basicMsg.StructMsg(
                    functor="schema_target",
                    arguments=[Utils.fromListToArgumentMsg(schema.targets)]
            )))
            
            for i, attr in enumerate(schema.attributes):
                clauses.append(wrapInClause(
                    basicMsg.StructMsg(
                        functor="attribute",
                        arguments=[
                            Utils.buildConstantArgumentMsg(i),
                            Utils.buildConstantArgumentMsg(attr.name),
                            attr.typeToArgumentMsg()]
                )))
            
            for i in range(dataset.shape[0]):
                values = list(map(
                    lambda x: Utils.buildConstantArgumentMsg(Utils.stringsConverter(x)),
                    [tf.get_static_value(x) for x in dataset[i].values()]))
                clauses.append(wrapInClause(
                    basicMsg.StructMsg(
                        functor=schema.name,
                        arguments=values
                )))
            
            yield request.replySuccess(
                sideEffects = [SideEffectMsg(
                    clauses = SetClausesOfKBMsg(
                        kbType = SetClausesOfKBMsg.DYNAMIC,
                        operationType = SetClausesOfKBMsg.ADD, 
                        clauses = clauses
                        ))],
                hasNext=False)
        else:
            yield request.replyFail()
            
            
theoryFromDatasetPrimitive = DistributedElements.DistributedPrimitiveWrapper("theory_from_dataset", 2, __TheoryFromDatasetPrimitive())