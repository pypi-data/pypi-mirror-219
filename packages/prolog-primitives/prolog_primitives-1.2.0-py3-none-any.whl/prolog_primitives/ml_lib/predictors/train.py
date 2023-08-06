from prolog_primitives.basic import DistributedElements
from typing import Generator
from prolog_primitives.basic import Utils
from ..collections import SharedCollections
import tensorflow as tf
from datasets import Dataset

def parseParams(structs: list[Utils.Struct]):
    params = {
        "epoch": 1,
        "loss": "mse",
        "batch": None,
        "learning_rate": 0.001
    }
    for struct in structs:
        if(struct.functor == "max_epoch"):
            params['epoch'] = int(struct.arguments[0])
        elif(struct.functor == "batch_size"):
            params['batch'] = int(struct.arguments[0])
        elif(struct.functor == "learning_rate"):
            params['learning_rate'] = struct.arguments[0]
        elif(struct.functor == "loss"):
            loss = struct.arguments[0]
            if(loss == "cross_entropy"):
                params['loss'] = tf.keras.losses.BinaryCrossentropy()
            else: 
                params['loss'] = loss
    return params

class __Train(DistributedElements.DistributedPrimitive):
    
    def solve(self, request: DistributedElements.DistributedRequest) -> Generator[DistributedElements.DistributedResponse, None, None]:
        predictor_in_ref = request.arguments[0]
        dataset_ref = request.arguments[1]
        params = request.arguments[2]
        predictor_out_ref = request.arguments[3]
        
        if(not predictor_in_ref.HasField('var') and not dataset_ref.HasField('var') and
           not params.HasField('var') and predictor_out_ref.HasField('var')):
            model: tf.keras.Model = SharedCollections().getModel(Utils.parseArgumentMsg(predictor_in_ref))
            datasetId = Utils.parseArgumentMsg(dataset_ref)
            dataset: Dataset = SharedCollections().getDataset(datasetId)
            schema = SharedCollections().getSchema(SharedCollections().getSchemaIdFromDataset(datasetId))
            
            params = Utils.parseArgumentMsg(params)
            if(type(params) is list):
                params = parseParams(params)
            else:
                params = parseParams(list())
            input = list()
            output = list()
            for attr in dataset.column_names:
                if(attr in schema.targets):
                    output.append(tf.cast(dataset[attr], tf.float32))
                else:
                    input.append(tf.cast(dataset[attr], tf.float32))
            
            output = tf.stack(output, axis = 1)
            input = tf.stack(input, axis = 1)
            optimizer = tf.keras.optimizers.Adam(learning_rate=params["learning_rate"])
            
            model.compile(
                loss = params["loss"],
                optimizer=optimizer,
                metrics=['mae'],
            )
            model.fit(x=input,y=output,  epochs=params["epoch"], validation_split=0.05)
            
            id = SharedCollections().addModel(model)
            yield request.replySuccess(substitutions={
                predictor_out_ref.var: Utils.buildConstantArgumentMsg(id)
                }, hasNext=False)
        else:
            yield request.replyFail()
             
trainPrimitive = DistributedElements.DistributedPrimitiveWrapper("train", 4, __Train())