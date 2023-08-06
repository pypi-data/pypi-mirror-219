from prolog_primitives.generatedProto import basicMessages_pb2 as basicMsg
from prolog_primitives.basic import Utils
import pandas as pd
import tensorflow as tf

class Attribute:  
    name: str
    type = None
    vocab = []
    
    def __init__(self,
                 name: str,
                 type,
                 vocab = []):
        self.name = name
        self.type = type
        self.vocab = vocab 

    def typeToArgumentMsg(self) -> basicMsg.ArgumentMsg:
        if(self.vocab != []):
            vocab_msg = Utils.fromListToArgumentMsg(self.vocab)
            if("int" in str(self.type)):    
                return Utils.buildConstantArgumentMsg(
                    basicMsg.StructMsg(
                        functor="ordinal",
                        arguments = [vocab_msg]
                    )
                )
            else:
                return Utils.buildConstantArgumentMsg(
                    basicMsg.StructMsg(
                        functor="categorical",
                        arguments = [vocab_msg]
                    )
                )
        if("int" in str(self.type)):
            return Utils.buildConstantArgumentMsg("integer")
        elif("float" in str(self.type)):
            return Utils.buildConstantArgumentMsg("real")
        elif("str" in str(self.type)):
            return Utils.buildConstantArgumentMsg("string")
        elif("bool" in str(self.type)):
            return Utils.buildConstantArgumentMsg("boolean")
        
    def typeCastElement(self, element):
        if(self.vocab != []): 
            if(self.type == tf.string and element in self.vocab):
                return element
            elif(self.type == tf.int64 and int(element) in self.vocab):
                return int(element)
        elif(self.type == tf.int64):
            return int(float(element))
        elif(self.type == tf.float64):
            return float(element)
        elif(self.type == tf.string):
            return element
        elif(self.type == tf.bool):
            return bool(element)
            
def parseAttributeFromStruct(struct: Utils.Struct) -> Attribute:
    attr_infos = struct.arguments
    attr_name = attr_infos[1]
    type_struct = attr_infos[2]
    attr_vocab = []
    if(type_struct == "integer"):
        attr_type = tf.int64
    elif(type_struct == "real"):
        attr_type = tf.float64
    elif(type_struct == "string"):
        attr_type = tf.string
    elif(type_struct == "boolean"):
        attr_type = tf.bool
    elif(type(type_struct) is Utils.Struct):
        if(type_struct.functor == "categorical"):
            attr_type = tf.string
            attr_vocab = type_struct.arguments[0]
        else:
            attr_type = tf.int64
            attr_vocab = tuple(map(int, type_struct.arguments[0]))
    return Attribute(attr_name, attr_type, attr_vocab)

class Schema:
    name: str
    attributes: list[Attribute]
    targets: list[str]
    
    def __init__(self,
                 name: str,
                 attributes: list,
                 targets: list):
        self.name = name
        self.attributes = attributes
        self.targets = targets   
   