import grpc
from grpc._server import _Context as Context
from prolog_primitives.generatedProto import primitiveService_pb2_grpc as Server
from prolog_primitives.generatedProto import primitiveService_pb2 as primitivesMsg
from prolog_primitives.generatedProto import basicMessages_pb2 as basicMsg
from . import DistributedElements
from . import Session
from queue import Queue
from concurrent import futures
from . import DBManager

class GenericPrimitive(Server.GenericPrimitiveService):
    primitive: DistributedElements.DistributedPrimitive
    functor: str = ""
    arity: int = 0
    executor: futures.Executor
    
    def __init__(self, primitive: DistributedElements.DistributedPrimitive, functor: str, arity: int, executor):  
        self.primitive = primitive
        self.functor = functor
        self.arity = arity
        self.executor = executor

    def getSignature(self, request, context):
        signature = (self.functor, self.arity)
        return basicMsg.SignatureMsg(name=signature[0], arity=signature[1])

    def callPrimitive(self, request_iterator, context: Context):
        queue = Queue[primitivesMsg.GeneratorMsg]()
        def messageHandling():
            session: Session.ServerSession = None
            for value in request_iterator:
                msg: primitivesMsg.SolverMsg = value
                if(session == None and msg.request.IsInitialized()):
                    session = Session.ServerSession(
                        primitive = self.primitive,
                        request = msg.request,
                        queue = queue)
                else:
                    self.executor.submit(session.handleMessage, msg)
        self.executor.submit(messageHandling)
        
        context.add_callback(lambda: queue.put(None))
        
        while context.is_active():
            msg: primitivesMsg.GeneratorMsg = queue.get()
            if(msg != None):
                yield msg
            else:
                context.cancel()

def serve(primitive: DistributedElements.DistributedPrimitiveWrapper, port: int = 8080, libraryName: str = "", withDB: bool = False):
    executor = futures.ThreadPoolExecutor(32)
    service = GenericPrimitive(primitive.primitive, primitive.functor, primitive.arity, executor)
    server = grpc.server(executor)
    Server.add_GenericPrimitiveServiceServicer_to_server(service, server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    if(withDB):
        DBManager.addPrimitive(service.functor, service.arity, libraryName, "localhost", port)
    print("Server started, listening on " + str(port))
    return server
        

        
        

