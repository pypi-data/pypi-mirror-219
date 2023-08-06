import sys
sys.path.append('../generatedProto')
from abc import ABC, abstractmethod

from prolog_primitives.generatedProto import primitiveService_pb2 as primitiveMsg
from prolog_primitives.generatedProto import basicMessages_pb2 as basicMsg
from concurrent.futures import Future

class SubRequestEvent(ABC):
    
    id: str
    msg: primitiveMsg.GeneratorMsg
    
    @abstractmethod
    def signalResponse(self, msg: primitiveMsg.SubResponseMsg):
        pass
    
    @abstractmethod
    def awaitResult(self):
        pass

class ReadLineEvent(SubRequestEvent):
    id: str
    msg: primitiveMsg.GeneratorMsg
    future: Future[primitiveMsg.LineMsg]
    
    def __init__(self, id: str, channelName: str):
        self.id = id
        self.msg = primitiveMsg.GeneratorMsg(
            request = primitiveMsg.SubRequestMsg(
                id = id,
                readLine = primitiveMsg.ReadLineMsg(
                    channelName=channelName
                    )))
        self.future = Future()
    
    def signalResponse(self, msg: primitiveMsg.SubResponseMsg):
        self.future.set_result(msg.line)
    
    def awaitResult(self) -> str:
        return self.future.result().content
    
class SingleSubSolveEvent(SubRequestEvent):
    id: str
    msg: primitiveMsg.GeneratorMsg
    future: Future[primitiveMsg.ResponseMsg]
    
    def __init__(self, id: str, query: basicMsg.StructMsg, timeout: int):
        self.id = id
        self.msg = primitiveMsg.GeneratorMsg(
            request = primitiveMsg.SubRequestMsg(
                id = id,
                subSolve = primitiveMsg.SubSolveRequest(
                    query = query,
                    timeout = timeout
                    )))
        self.future = Future()
    
    def signalResponse(self, msg: primitiveMsg.SubResponseMsg):
        self.future.set_result(msg.solution)
    
    def awaitResult(self) -> primitiveMsg.ResponseMsg:
        return self.future.result()
    
from enum import Enum
    
class SingleInspectKBEvent(SubRequestEvent):  
    
    id: str
    msg: primitiveMsg.GeneratorMsg
    future: Future[basicMsg.StructMsg]
    
    def __init__(
        self, 
        id: str,
        kbType: primitiveMsg.InspectKbMsg.KbType,
        maxClauses: int,
        filters: list[tuple[primitiveMsg.InspectKbMsg.FilterType, str]]
        ):
        filtersMsg = list(map(
            lambda pair: primitiveMsg.InspectKbMsg.FilterMsg(type = pair[0], argument = pair[1]),
            filters))
        self.id = id
        self.msg = primitiveMsg.GeneratorMsg(
            request = primitiveMsg.SubRequestMsg(
                id = id,
                inspectKb = primitiveMsg.InspectKbMsg(
                    kbType=kbType, maxClauses=maxClauses, filters=filtersMsg
                    )
                )
            )
        self.future = Future()
    
    def signalResponse(self, msg: primitiveMsg.SubResponseMsg):
        self.future.set_result(msg.clause)
    
    def awaitResult(self) -> basicMsg.StructMsg:
        return self.future.result()
    
class GenericGet(SubRequestEvent):  
    
    id: str
    msg: primitiveMsg.GeneratorMsg
    future: Future[primitiveMsg.GenericGetResponse]
    
    def __init__(
        self, 
        id: str,
        type: primitiveMsg.GenericGetMsg.Element
        ):
        self.id = id
        self.msg = primitiveMsg.GeneratorMsg(
            request = primitiveMsg.SubRequestMsg(
                id = id,
                genericGet = primitiveMsg.GenericGetMsg(
                    element = type
                    )
                )
            )
        self.future = Future()
    
    def signalResponse(self, msg: primitiveMsg.SubResponseMsg):
        self.future.set_result(msg.genericGet)
    
    def awaitResult(self) -> primitiveMsg.GenericGetResponse:
        return self.future.result()

        