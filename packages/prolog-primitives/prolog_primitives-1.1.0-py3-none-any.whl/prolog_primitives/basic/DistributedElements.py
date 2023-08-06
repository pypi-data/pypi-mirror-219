import sys

from abc import ABC, abstractmethod
from typing import Generator
from prolog_primitives.generatedProto import sideEffectsMessages_pb2 as sideEffectsMsg
from prolog_primitives.generatedProto import primitiveService_pb2 as primitivesMsg
from prolog_primitives.generatedProto import basicMessages_pb2 as basicMsg
from prolog_primitives.generatedProto import errorsMessages_pb2 as errorMsg
import math

class DistributedRequest:
    functor: str
    arity: int
    arguments: list[basicMsg.ArgumentMsg]
    context: basicMsg.ExecutionContextMsg
    session = None
    query: basicMsg.StructMsg
    
    def __init__(self, functor: str, arity: int, arguments: list[basicMsg.ArgumentMsg],
                 context: basicMsg.ExecutionContextMsg, session):
        self.functor = functor
        self.arity = arity
        self.arguments = arguments
        self.context = context
        self.session = session
        self.query = basicMsg.StructMsg(functor=functor, arguments=arguments)
        

    def replyWith(self, condition: bool, sideEffects: sideEffectsMsg.SideEffectMsg = None, hasNext = True): 
        if condition:
            type = primitivesMsg.SolutionMsg.SUCCESS
        else:
            type = primitivesMsg.SolutionMsg.FAIL
        return DistributedResponse(
            primitivesMsg.SolutionMsg(
                query = self.query,
                type = type,
                hasNext = hasNext),
            sideEffects=sideEffects
        )
        
    def replySuccess(self, substitutions = None,  sideEffects: list[sideEffectsMsg.SideEffectMsg] = None, hasNext = True):
        return DistributedResponse(
            primitivesMsg.SolutionMsg(
                query = self.query,
                substitutions = substitutions,
                type =  primitivesMsg.SolutionMsg.SUCCESS,
                hasNext = hasNext),
            sideEffects=sideEffects
        )
        
    def replyFail(self, sideEffects: list[sideEffectsMsg.SideEffectMsg] = None, hasNext = False):
        return DistributedResponse(
            primitivesMsg.SolutionMsg(
                query = self.query, 
                type =  primitivesMsg.SolutionMsg.FAIL,
                hasNext = hasNext),
            sideEffects=sideEffects
        )
        
    def replyError(self, error: primitivesMsg.ErrorMsg,  sideEffects: sideEffectsMsg.SideEffectMsg = None, hasNext = False):
        return DistributedResponse(
            primitivesMsg.SolutionMsg(
                query = self.query,
                error = error,
                type = primitivesMsg.SolutionMsg.HALT,
                hasNext = hasNext),
            sideEffects=sideEffects
        )
        
    def subSolve(self, query: basicMsg.StructMsg, timeout: int = sys.maxsize) -> Generator[primitivesMsg.SolutionMsg, None, None]:
        return self.session.subSolve(query, timeout)
        
    def readLine(self, channelName: str) -> str:
        return self.session.readLine(channelName)    
    
    def inspectKb(
        self,
        kbType: primitivesMsg.InspectKbMsg.KbType,
        filters: list[tuple[primitivesMsg.InspectKbMsg.FilterType, str]],
        maxClauses: int = -1
        ) -> Generator[basicMsg.StructMsg, None, None]:
        return self.session.inspectKb(kbType, maxClauses, filters)
    
    def getElement(
        self,
        type: primitivesMsg.GenericGetMsg.Element
    ) -> primitivesMsg.GenericGetResponse:
        return self.session.genericGet(type)

class DistributedResponse:
    solution: primitivesMsg.SolutionMsg
    sideEffects: list[sideEffectsMsg.SideEffectMsg]
    
    def __init__(self, solution: primitivesMsg.SolutionMsg,  sideEffects: list[sideEffectsMsg.SideEffectMsg]):
        self.solution = solution
        self.sideEffects = sideEffects
        
        
class DistributedPrimitive(ABC):
    @abstractmethod
    def solve(self, request: DistributedRequest) -> Generator[DistributedResponse, None, None]:
        pass
    
class DistributedPrimitiveWrapper:
    functor: str
    arity: int
    primitive: DistributedPrimitive
    
    def __init__(self, functor: str,  arity: int, primitive: DistributedPrimitive):
        self.functor = functor
        self.arity = arity
        self.primitive = primitive