from prolog_primitives.basic import DistributedElements
from typing import Generator
from prolog_primitives.basic import Utils
from ..collections import SharedCollections
import tensorflow as tf
from datasets import Dataset

class __Predict(DistributedElements.DistributedPrimitive):
    
    def solve(self, request: DistributedElements.DistributedRequest) -> Generator[DistributedElements.DistributedResponse, None, None]:
        predictor_ref = request.arguments[0]
        dataset_ref = request.arguments[1]
        prediction_ref = request.arguments[2]
        
        if(not predictor_ref.HasField('var') and not dataset_ref.HasField('var') and
           prediction_ref.HasField('var')):
            model: tf.keras.Model = SharedCollections().getModel(Utils.parseArgumentMsg(predictor_ref))
            
            data = None
            
            datasetId = Utils.parseArgumentMsg(dataset_ref)
            dataset: Dataset = SharedCollections().getDataset(datasetId)
            if(dataset != None):
                schemaId = SharedCollections().getSchemaIdFromDataset(datasetId)
                schema = SharedCollections().getSchema(schemaId)
                data = list()
                for attr in dataset.column_names:
                    if(not attr in schema.targets):
                        data.append(tf.cast(dataset[attr], tf.float32))
                data = tf.stack(data, axis = 1)
                result = {}
                for attr in schema.targets:
                    result[attr] = []
                for row in model.predict(x=data):
                    for attr, y in zip(schema.targets, row):
                        result[attr].append(y)
                dataset = Dataset.from_dict(result).with_format("tf")
                datasetId = SharedCollections().addDataset(dataset, schemaId)
            
                yield request.replySuccess(substitutions={
                    prediction_ref.var: Utils.buildConstantArgumentMsg(datasetId)
                    }, hasNext=False)
            else:
                row = [float(x) for x in Utils.parseArgumentMsg(dataset_ref).arguments]
                data = tf.constant(value=[row], dtype=tf.float32)
            
                result = model.predict(x=data)[0]
                yield request.replySuccess(substitutions={
                    prediction_ref.var: Utils.fromListToArgumentMsg(result.tolist())
                    }, hasNext=False)
        else:
            yield request.replyFail()
             
predictPrimitive = DistributedElements.DistributedPrimitiveWrapper("predict", 3, __Predict())