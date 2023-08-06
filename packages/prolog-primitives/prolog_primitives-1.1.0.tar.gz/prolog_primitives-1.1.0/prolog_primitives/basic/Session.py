import sys
sys.path.append('../generatedProto')

import random
import string
from prolog_primitives.generatedProto import primitiveService_pb2 as primitivesMsg
from prolog_primitives.generatedProto import basicMessages_pb2 as basicMsg
from . import SubRequestEvent
from . import DistributedElements
from typing import Generator
from queue import Queue

class ServerSession:
    stream: Generator[primitivesMsg.GeneratorMsg, None, None]
    ongoingSubRequests: list[SubRequestEvent.SubRequestEvent] = list()
    msgQueue: Queue[primitivesMsg.GeneratorMsg]
    request: DistributedElements.DistributedRequest
    
    def __init__(self,
                 primitive: DistributedElements.DistributedPrimitive,
                 request: primitivesMsg.RequestMsg,
                 queue:  Queue[primitivesMsg.GeneratorMsg]):
        self.msgQueue = queue
        self.request = DistributedElements.DistributedRequest(
            functor = request.signature.name,
            arity = request.signature.arity,
            arguments = request.arguments,
            context = request.context, 
            session = self)
        self.stream = primitive.solve(
            request = self.request
        )

    def handleMessage(self, msg: primitivesMsg.SolverMsg):
        #Compute Next Solution
        if msg.HasField("next"):
            try:
                nextValue: DistributedElements.DistributedResponse = next(self.stream)
            except:
                e = sys.exc_info()
                print(e)
                import traceback
                print(traceback.format_exc())
                nextValue: DistributedElements.DistributedResponse = self.request.replyFail()
            self.msgQueue.put(
                primitivesMsg.GeneratorMsg(
                    response=primitivesMsg.ResponseMsg(
                        solution = nextValue.solution, sideEffects= nextValue.sideEffects)
                )
            )
        #Handle response from subrequest
        elif msg.HasField("response"):
            subResponse: primitivesMsg.SubResponseMsg = msg.response
            event: SubRequestEvent.SubRequestEvent = list(
                filter(lambda temp: temp.id == subResponse.id, self.ongoingSubRequests)).pop()
            if(event != None):
                event.signalResponse(subResponse)
                self.ongoingSubRequests.remove(event)
                
        
    def subSolve(self, query: basicMsg.StructMsg, timeout: int) -> Generator[primitivesMsg.SolutionMsg, None, None]: 
        id = self.idGenerator()
        hasNext = True
        while hasNext:
            event: SubRequestEvent.SingleSubSolveEvent = SubRequestEvent.SingleSubSolveEvent(
                id = id,
                query = query,
                timeout = timeout)
            self.ongoingSubRequests.append(event)
            self.msgQueue.put(item = event.msg)
            result = event.awaitResult()
            hasNext = result.solution.hasNext
            yield result.solution
        
    def readLine(self, channelName: str) -> str:
        event: SubRequestEvent.ReadLineEvent = SubRequestEvent.ReadLineEvent(self.idGenerator(), channelName)
        self.ongoingSubRequests.append(event)
        self.msgQueue.put(item = event.msg)
        result = event.awaitResult()
        return result
    
    def inspectKb(
        self,
        kbType: primitivesMsg.InspectKbMsg.KbType,
        maxClauses: int,
        filters: list[tuple[primitivesMsg.InspectKbMsg.FilterType, str]]
        ) -> Generator[basicMsg.StructMsg, None, None]: 
        id = self.idGenerator()
        hasNext = True
        while hasNext:
            event: SubRequestEvent.SingleInspectKBEvent = SubRequestEvent.SingleInspectKBEvent(
                id = id,
                kbType = kbType,
                maxClauses = maxClauses,
                filters = filters
                )
            self.ongoingSubRequests.append(event)
            self.msgQueue.put(item = event.msg)
            result = event.awaitResult()
            if(result.functor != "" and len(result.arguments) != 0):
                hasNext = True
                yield result
            else:
                hasNext = False
                yield None
            
    def genericGet(self, type: primitivesMsg.GenericGetMsg.Element) -> primitivesMsg.GenericGetResponse:
        event: SubRequestEvent.GenericGet = SubRequestEvent.GenericGet(self.idGenerator(), type)
        self.ongoingSubRequests.append(event)
        self.msgQueue.put(item = event.msg)
        result = event.awaitResult()
        return result
    
    def idGenerator(self) -> str:
        characters = string.ascii_letters + string.digits
        id = ''.join(random.choice(characters) for i in range(10)) 
        while(len(list(filter(lambda temp: temp.id == id, self.ongoingSubRequests))) != 0):
            id = ''.join(random.choice(characters) for i in range(10)) 
        return id 