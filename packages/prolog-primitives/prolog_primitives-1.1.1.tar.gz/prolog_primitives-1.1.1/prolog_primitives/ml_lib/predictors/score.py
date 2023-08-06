from prolog_primitives.basic import DistributedElements
from typing import Generator
from prolog_primitives.basic import Utils
from ..collections import SharedCollections
import tensorflow as tf
from ..schema.schemaClass import Schema
from abc import ABC, abstractmethod
import numpy as np



class __AssessTemplate(DistributedElements.DistributedPrimitive, ABC):
    
    @abstractmethod
    def evaluator(self, y_true, y_pred):
        pass
    
    def solve(self, request: DistributedElements.DistributedRequest) -> Generator[DistributedElements.DistributedResponse, None, None]:
        y_true_ref = request.arguments[0]
        y_pred_ref = request.arguments[1]
        score = request.arguments[2]
        
        if(not y_true_ref.HasField('var') and not y_pred_ref.HasField('var') and
           score.HasField('var')):
            
            def parseY(input):
                if(type(input) is str):
                    dataset = SharedCollections().getDataset(input)
                    schema: Schema = SharedCollections().getSchema(SharedCollections().getSchemaIdFromDataset(input))
                    y = {}
                    for attr in dataset.column_names:
                        if(attr in schema.targets):
                            y[attr] = list(tf.get_static_value(dataset[attr]))
                    return y
                elif(type(input[0]) is list):
                    y = {}
                    lenght_1 = len(input[0])
                    lenght_2 = len(input)
                    input = np.reshape(input, (lenght_1, lenght_2))
                    
                    for x in range(len(input)):
                        y[f"target{x}"] = list(input[x])
                        
                    return y
                else:
                    return [float(x) for x in input]
                
            y_true = parseY(Utils.parseArgumentMsg(y_true_ref))
                    
            y_pred = parseY(Utils.parseArgumentMsg(y_pred_ref))   
            scores = []   
            for (attr1, y1), (attr2, y2) in zip(y_true.items(), y_pred.items()):
                scores.append(self.evaluator(y1, y2))
            
            totalscore = tf.get_static_value(sum(scores)/len(scores))
            
            yield request.replySuccess(substitutions={
                score.var:Utils.buildConstantArgumentMsg(totalscore)
            }, hasNext=False)

        else:
            yield request.replyFail()
            
class __Mse(__AssessTemplate):
    
    def evaluator(self, y_true, y_pred):
        m = tf.keras.metrics.MeanSquaredError()
        m.update_state(y_true, y_pred)
        return m.result().numpy()
                 
msePrimitive = DistributedElements.DistributedPrimitiveWrapper("mse", 3, __Mse())


class __Mae(__AssessTemplate):
    
    def evaluator(self, y_true, y_pred):
        m = tf.keras.metrics.MeanAbsoluteError()
        m.update_state(y_true, y_pred)
        return m.result().numpy()
                 
maePrimitive = DistributedElements.DistributedPrimitiveWrapper("mae", 3, __Mae())

class __R(__AssessTemplate):
    
    def evaluator(self, y_true, y_pred):
        m = tf.keras.metrics.RootMeanSquaredError()
        m.update_state(y_true, y_pred)
        return m.result().numpy()
                 
rPrimitive = DistributedElements.DistributedPrimitiveWrapper("r", 3, __R())


class __Recall(__AssessTemplate):
    
    def evaluator(self, y_true, y_pred):
        m = tf.keras.metrics.Recall()
        m.update_state(y_true, y_pred)
        return m.result().numpy()
                 
recallPrimitive = DistributedElements.DistributedPrimitiveWrapper("recall", 3, __Recall())


class __Accuracy(__AssessTemplate):
    
    def evaluator(self, y_true, y_pred):
        m = tf.keras.metrics.Accuracy()
        m.update_state(y_true, y_pred)
        return m.result().numpy()
                 
accuracyPrimitive = DistributedElements.DistributedPrimitiveWrapper("accuracy", 3, __Accuracy())