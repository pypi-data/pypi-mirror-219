from prolog_primitives.basic import DistributedElements
from typing import Generator
from prolog_primitives.basic import Utils
from ..collections import SharedCollections
from datasets import Dataset



class __Classify(DistributedElements.DistributedPrimitive):
    
    def solve(self, request: DistributedElements.DistributedRequest) -> Generator[DistributedElements.DistributedResponse, None, None]:
        prediction_ref = request.arguments[0]
        strategy = request.arguments[1]
        classes = request.arguments[2]
        classification_ref = request.arguments[3]
        
        if(not prediction_ref.HasField('var') and not strategy.HasField('var') and
           not classes.HasField('var') and classification_ref.HasField('var')):
            
            classes = Utils.parseArgumentMsgList(classes)
            strategy = Utils.parseArgumentMsg(strategy)
            
            def classify(row):
                if(strategy == "argmax"):
                    max = None
                    current_class = "UKN"
                    for value, x in zip(row, classes):
                        if(max == None or value > max):
                            max = value
                            current_class = x
                    return current_class
                elif(float(strategy.arguments[0])):
                    threshold = float(strategy.arguments[0])
                    listOfLabels = []
                    for value, x in zip(row, classes):
                        if(value > threshold):
                            listOfLabels.append(x)
                    return listOfLabels
            
            
            predictionId = Utils.parseArgumentMsg(prediction_ref)
            prediction: Dataset = SharedCollections().getDataset(str(predictionId))
            if(prediction != None):
                classification = []
                for row in prediction:
                    
                    classification.append(classify(row.values()))
                    
                
                    
                dataset = Dataset.from_dict({"labels":classification}).with_format("tf")
                datasetId = SharedCollections().addDataset(dataset, None)
                yield request.replySuccess(substitutions={
                    classification_ref.var: Utils.buildConstantArgumentMsg(datasetId)
                    }, hasNext=False)
            else:
                row = [float(x) for x in Utils.parseArgumentMsgList(prediction_ref)]
                result = classify(row)
                if(type(result) == list):
                    result = Utils.fromListToArgumentMsg(result)
                else:
                    result = Utils.buildConstantArgumentMsg(result)
                
                yield request.replySuccess(substitutions={
                    classification_ref.var: result
                    }, hasNext=False)

        else:
            yield request.replyFail()
             
classifyPrimitive = DistributedElements.DistributedPrimitiveWrapper("classify", 4, __Classify())