from prolog_primitives.basic import DistributedElements
from prolog_primitives.generatedProto import primitiveService_pb2 as primitiveMsg
from typing import Generator
from prolog_primitives.basic import Utils
from .. import collections
from .schemaClass import parseAttributeFromStruct

class __TheoryToSchemaPrimitive(DistributedElements.DistributedPrimitive):
    
    def solve(self, request: DistributedElements.DistributedRequest) -> Generator[DistributedElements.DistributedResponse, None, None]:
        arg0 = request.arguments[0]
        if(arg0.HasField("var")):
            schema_name = str(Utils.parseArgumentMsg(
                next(request.inspectKb(
                    primitiveMsg.InspectKbMsg.STATIC,
                    [(primitiveMsg.InspectKbMsg.STARTS_WITH, "schema_name")])
                ).arguments[0].struct.arguments[0]
            ))
                        
            attributes = list()
            for i in request.inspectKb(
                primitiveMsg.InspectKbMsg.STATIC,
                [(primitiveMsg.InspectKbMsg.STARTS_WITH, "attribute")]):    
                if(i == None and len(attributes) == 0 ):
                    yield request.replyFail()
                elif(i != None):
                    fact = Utils.parseStructMsg(i.arguments[0].struct)
                    index = int(fact.arguments[0])
                    attributes.insert(index, parseAttributeFromStruct(fact))
                 
            targets = list()     
            targetFact = next(request.inspectKb(
                primitiveMsg.InspectKbMsg.STATIC,
                [(primitiveMsg.InspectKbMsg.STARTS_WITH, "schema_target")]))
            if(targetFact == None):
                yield request.replyFail()
            else:
                targets = Utils.parseArgumentMsgList(targetFact.arguments[0].struct.arguments[0])
            substitutions = {
                arg0.var: Utils.buildConstantArgumentMsg(collections
                                               .SharedCollections()
                                               .addSchema(collections.Schema(schema_name, attributes, targets))) 
                }
            yield request.replySuccess(substitutions, hasNext=False)
        else:
            request.replyFail()
            
            
theoryToSchemaPrimitive = DistributedElements.DistributedPrimitiveWrapper("theory_to_schema", 1, __TheoryToSchemaPrimitive())