from .schema.schema import schemaPrimitive
from .schema.theoryToSchema import theoryToSchemaPrimitive
from .dataset.theoryToDataset import theoryToDatasetPrimitive
from .dataset.randomSplit import randomSplitPrimitive
from .dataset.column import columnPrimitive
from .dataset.row import rowPrimitive
from .dataset.cell import cellPrimitive
from .dataset.fold import foldPrimitive
from .dataset.theory_from_Dataset import theoryFromDatasetPrimitive
from .transformations.schema_trasformation import schemaTrasformation
from .transformations.normalization import normalizePrimitive
from .transformations.one_hot_encode import one_hot_encodePrimitive
from .transformations.drop import dropPrimitive
from .transformations.fit import fitPrimitive
from .transformations.transform import transformPrimitive
from .neuralNetwork.inputLayer import inputLayerPrimitive
from .neuralNetwork.denseLayer import denseLayerPrimitive
from .neuralNetwork.outputLayer import outputLayerPrimitive
from .neuralNetwork.neuralNetwork import neuralNetworkPrimitive
from .predictors.train import trainPrimitive
from .predictors.predict import predictPrimitive
from .predictors.classify import classifyPrimitive
from .predictors.score import msePrimitive, maePrimitive, accuracyPrimitive, recallPrimitive, rPrimitive
from ..basic import PrimitiveWrapper, DistributedElements
from concurrent.futures import ThreadPoolExecutor

def main():
    servers = []
    libraryName = "customLibrary"

    def launchPrimitive(primitive: DistributedElements.DistributedPrimitiveWrapper, port: int):
        server = PrimitiveWrapper.serve(primitive, port, libraryName)
        servers.append(server)
        #server.wait_for_termination()
        
    primitives = [schemaPrimitive, theoryToSchemaPrimitive,
                theoryToDatasetPrimitive, randomSplitPrimitive,
                rowPrimitive, columnPrimitive, cellPrimitive, foldPrimitive, 
                theoryFromDatasetPrimitive, schemaTrasformation,
                normalizePrimitive, one_hot_encodePrimitive, dropPrimitive,
                fitPrimitive, transformPrimitive, inputLayerPrimitive,
                denseLayerPrimitive, outputLayerPrimitive, neuralNetworkPrimitive,
                trainPrimitive, predictPrimitive, classifyPrimitive, msePrimitive,
                maePrimitive, accuracyPrimitive, recallPrimitive, rPrimitive]

    initialport = 8080
    port = initialport
    executor = ThreadPoolExecutor(max_workers=len(primitives))

    for primitive in primitives:
        #future = executor.submit(launchPrimitive, primitive, port)
        launchPrimitive(primitive, port)
        port += 1

    print(f"Servers listening from {initialport} to {port-1}")

    try:
        for server in servers:
            server.wait_for_termination()
    except (Exception, KeyboardInterrupt, SystemExit) as inst:
        executor.shutdown(wait=False, cancel_futures=True)
        for server in servers:
            server.stop(0)

    #for primitive in primitives:
    #    DBManager.deletePrimitive(primitive.functor, primitive.arity, libraryName)
    print("Done!")