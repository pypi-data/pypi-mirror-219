from abc import ABC, abstractmethod
import tensorflow as tf
from ..collections import SharedCollections
from ..schema.schemaClass import Schema
from datasets import Dataset
import itertools

class Transformation(ABC):
    applier = None
    inverter = None
    
    @abstractmethod
    def copy(self):
        pass
    
class Normalization(Transformation):
    
    applier = tf.keras.layers.Normalization()
    inverter = tf.keras.layers.Normalization(invert=True)
        
    def adapt(self, inputs):
        self.applier.adapt(inputs)
        self.inverter.adapt(inputs)
        
    def copy(self):
        return Normalization()
    
class OneHotEncoder(Transformation):
    
    vocab: list[str] = None
        
    def __init__(self,
                 vocab: list[str]):
        self.vocab = vocab
        self.applier = tf.keras.layers.StringLookup(vocabulary=vocab)
        self.inverter = tf.keras.layers.StringLookup(vocabulary=vocab, invert=True)

        
    def copy(self):
        return OneHotEncoder(self.vocab)
            
class Dropper(Transformation):
    
    applier = lambda x: None
    inverter = lambda x: None
    
    def copy(self):
        return Dropper()      
    
class Pipeline:   
    originalSchemaId: str = None
    originalSchema: Schema = None
    __layers: dict

    def __init__(self,
                 originalSchema: str,
                 layers: dict = {}):
        self.originalSchemaId = originalSchema 
        self.originalSchema = SharedCollections().getSchema(originalSchema)
        self.__layers = {}
        for attr in self.originalSchema.attributes:
            self.__layers[attr.name] = [] + layers.get(attr.name, [])
        
    def append(self, pipeline: dict):
        new_pipeline = {}
        for attr, layers in self.__layers.items():
            new_pipeline[attr] = layers + pipeline.get(attr, [])
        return Pipeline(self.originalSchemaId, new_pipeline)    
    
    def adapt(self, inputs):
        newLayers = dict.fromkeys(self.__layers.keys())
        for attr, layers in self.__layers.items():
            data = tf.reshape(inputs[attr], (len(inputs[attr]), -1))
            newLayers[attr] = []
            for layer in layers:
                copied = layer.copy()
                if(type(copied) == Normalization):
                    copied.adapt(data)
                data = copied.applier(data)
                newLayers[attr].append(copied)
        return Pipeline(self.originalSchemaId, newLayers)
        
    def apply(self, inputs):
        output = {}
        for attr, layers in self.__layers.items():
            output[attr] = tf.reshape(inputs[attr], (len(inputs[attr]), -1))
            for layer in layers:  
                output[attr] = layer.applier(output[attr])

            
            
        return Dataset.from_dict(output)
        
    def invert(self, inputs):
        output = {}
        for attr, layers in self.__layers.items():
            reversedList = list(layers)
            reversedList.reverse()
            output[attr] = tf.reshape(inputs[attr], (len(inputs[attr]), -1))
            for layer in reversedList:  
                output[attr] = layer.inverter(output[attr])
        return Dataset.from_dict(output)
    
    def computeFinalSchema(self) -> Schema:
        from ..schema.schemaClass import Attribute, Schema
        data = {}
        for attr in self.originalSchema.attributes:
            data[attr.name] = {
                "dtype": attr.type,
                "shape": tf.TensorShape([1,])
            }
            
        attributes = []
        for attr, layers in self.__layers.items():
            for layer in layers:
                if(type(layer) == Dropper):
                    del data[attr]
                else:
                    data[attr] = {
                        "dtype": layer.applier.dtype,
                        "shape": layer.applier.compute_output_shape(data[attr]["shape"])
                    }
            try:
                if(data[attr]['shape'][1] > 1):
                    for i in range(attr['shape'][1]):
                        attributes.append(
                            Attribute(str(attr)+"_"+str(i), tf.as_dtype(data[attr]['dtype']))
                    )
            except:
                if(attr in data):
                    attributes.append(
                        Attribute(attr, tf.as_dtype(data[attr]['dtype']))
                    )
        
        newTargets = list(set(data.keys()).intersection(self.originalSchema.targets))
        
        return Schema(self.originalSchema.name, attributes, newTargets)