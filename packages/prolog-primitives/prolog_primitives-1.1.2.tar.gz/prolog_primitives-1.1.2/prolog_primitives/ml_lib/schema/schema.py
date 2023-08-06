from prolog_primitives.basic import DistributedElements
from prolog_primitives.generatedProto import basicMessages_pb2 as basicMsg
from typing import Generator
from prolog_primitives.basic import Utils
from ..collections import SharedCollections
from .schemaClass import Schema, Attribute, parseAttributeFromStruct

class __SchemaPrimitive(DistributedElements.DistributedPrimitive):
    
    def solve(self, request: DistributedElements.DistributedRequest) -> Generator[DistributedElements.DistributedResponse, None, None]:
        schema_ref = request.arguments[0]
        schema_name = request.arguments[1]
        attributes = request.arguments[2]
        targets = request.arguments[3]

        #First Case of only retrieving infos on existing schema
        if(not schema_ref.HasField("var") and schema_name.HasField("var") and attributes.HasField("var") and targets.HasField("var")):
            schema: Schema = SharedCollections().getSchema(str(Utils.parseArgumentMsg(schema_ref)))
            if(schema != None):
                name_fact = Utils.buildConstantArgumentMsg(schema.name)
                attributes_facts = list[basicMsg.StructMsg]()
                i: int = 0
                
                for attr in schema.attributes:
                    attribute = [
                        Utils.buildConstantArgumentMsg(i),
                        Utils.buildConstantArgumentMsg(attr.name),
                        attr.typeToArgumentMsg()
                    ]
                    attributes_facts.append(
                        basicMsg.StructMsg(
                            functor = "attribute",
                            arguments = attribute
                        )
                    )
                    i += 1 
                yield request.replySuccess(substitutions = {
                    schema_name.var: name_fact,
                    attributes.var: Utils.fromListToArgumentMsg(attributes_facts),
                    targets.var: Utils.fromListToArgumentMsg(schema.targets)
                })
            else:
                yield request.replyFail()
        elif(not schema_name.HasField("var") and not attributes.HasField("var") and not targets.HasField("var")):
            #Parsing attributes
            attributes = Utils.parseArgumentMsgList(attributes)
            attributesList = list[Attribute]()
            for attr in attributes:
                attributesList.insert(int(attr.arguments[0]), parseAttributeFromStruct(attr))
            #Parsing targets
            targets =  Utils.parseArgumentMsgList(targets)
            targetsList = list(map(str, targets))
            id = SharedCollections().addSchema(
                Schema(str(Utils.parseArgumentMsg(schema_name)), attributesList, targetsList))
            yield request.replySuccess(substitutions={
                schema_ref.var:  Utils.buildConstantArgumentMsg(id)
            }, hasNext=False)
        else:
            yield request.replyFail()
            
schemaPrimitive = DistributedElements.DistributedPrimitiveWrapper("schema", 4, __SchemaPrimitive())