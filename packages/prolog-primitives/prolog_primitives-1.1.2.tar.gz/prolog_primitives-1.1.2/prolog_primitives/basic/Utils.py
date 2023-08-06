
from prolog_primitives.generatedProto import basicMessages_pb2 as basicMsg
import numbers

class Struct:
    functor: str
    arguments: list
    
    def __init__(self, functor: str, arguments: list):
        self.functor = functor
        self.arguments = arguments
        
    def __str__(self):
        term = self.functor + "("
        for arg in self.arguments:
            term += str(arg) + ","
        if(term[-1] == ","):
            return term[:-1] + ")"
        else:
            return term[:-1]

def parseArgumentMsg(msg: basicMsg.ArgumentMsg):
    if(msg.HasField("struct")):
        if(msg.struct.functor == "."):
            return parseArgumentMsgList(msg)
        else:   
            return parseStructMsg(msg.struct)
    elif(msg.HasField("var")):
        return msg.var
    elif(msg.HasField("numeric")):
        return msg.numeric
    elif(msg.HasField("atom")):
        return msg.atom
    
def parseStructMsg(msg: basicMsg.StructMsg):
    if(len(msg.arguments) > 0):
        arguments = list()
        for arg in msg.arguments:
            arguments.append(parseArgumentMsg(arg))
        return Struct(msg.functor, arguments)
    else:   
        return msg.functor
       
def parseArgumentMsgList(msg: basicMsg.ArgumentMsg) -> list:
    returnValue = list()
    currentValue = msg.struct
    while(len(currentValue.arguments) != 0):
        value = parseArgumentMsg(currentValue.arguments[0])
        if(value != "[" and value != "]"):
            returnValue.append(value)
        currentValue = currentValue.arguments[1].struct
    return returnValue 

def fromListToArgumentMsg(elements: list) -> basicMsg.ArgumentMsg:
    last_element = buildConstantArgumentMsg(
        basicMsg.StructMsg(
                functor = "[]"
            )
        )
    
    elements.reverse()
    for i in elements:
        current_element = basicMsg.StructMsg(
            functor="."
        )
        if(type(i) is basicMsg.StructMsg):
            current_element.arguments.append(
                buildConstantArgumentMsg(i)
            )
        elif(isinstance(i, numbers.Number)):
            current_element.arguments.append(
                buildConstantArgumentMsg(i)
            )
        elif(type(i) is str):
            current_element.arguments.append(
                buildConstantArgumentMsg(i)
            )
        current_element.arguments.append(
                last_element
            )
        last_element = buildConstantArgumentMsg(current_element)
    return last_element
      
def stringsConverter(x):
    if(type(x) is bytes):
        return str(x.decode('utf-8'))
    else:
        return float(x)

def buildConstantArgumentMsg(value):
    if(type(value) is str):
        return basicMsg.ArgumentMsg(atom=value)
    if(type(value) is basicMsg.StructMsg):
        return basicMsg.ArgumentMsg(struct=value)
    if(type(value) is bool):
        return basicMsg.ArgumentMsg(flag=value)
    if(isinstance(value, numbers.Number)):
        return basicMsg.ArgumentMsg(numeric=value)
