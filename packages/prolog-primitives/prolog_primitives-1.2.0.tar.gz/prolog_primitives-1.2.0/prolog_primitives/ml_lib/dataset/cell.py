from prolog_primitives.basic import DistributedElements
from typing import Generator
from prolog_primitives.basic import Utils
from ..collections import SharedCollections
import tensorflow as tf

class __CellPrimitive(DistributedElements.DistributedPrimitive):
    
    def solve(self, request: DistributedElements.DistributedRequest) -> Generator[DistributedElements.DistributedResponse, None, None]:
        dataset_ref = request.arguments[0]
        row_index = request.arguments[1]
        column_index = request.arguments[2]
        values = request.arguments[3]
        
        if(not dataset_ref.HasField("var") and values.HasField("var")):
            dataset = SharedCollections().getDataset(str(Utils.parseArgumentMsg(dataset_ref)))
                
            #Specific cell
            if(not row_index.HasField("var") and not column_index.HasField("var")): 
                row_index = int(Utils.parseArgumentMsg(row_index))
                column_index = Utils.parseArgumentMsg(column_index)
                if(type(column_index) is not str):
                    column_index = dataset.column_names[int(column_index)]
                value = Utils.stringsConverter(tf.get_static_value(dataset[row_index][column_index]))
                yield request.replySuccess({
                    values.var: Utils.buildConstantArgumentMsg(value)
                }, hasNext=False)
            
            #Cells in specific column    
            elif(not column_index.HasField("var")): 
                column_index = Utils.parseArgumentMsg(column_index)
                if(type(column_index) is not str):
                    column_index = dataset.column_names[int(column_index)]
                i = 0
                while(i < dataset.shape[0]):  
                    value = Utils.stringsConverter(tf.get_static_value(dataset[i][column_index]))
                    i += 1
                    yield request.replySuccess({
                        row_index.var: Utils.buildConstantArgumentMsg(i),
                        values.var: Utils.buildConstantArgumentMsg(value)
                    }, hasNext=i < dataset.shape[0])
                    
            #Cells in specific row        
            elif(not row_index.HasField("var")): 
                row_index = int(Utils.parseArgumentMsg(row_index))
                i = 0
                while(i < dataset.shape[1]):  
                    name = dataset.column_names[i]
                    
                    value = Utils.stringsConverter(tf.get_static_value(dataset[row_index][name]))
                    i += 1
                    yield request.replySuccess({
                        column_index.var: Utils.buildConstantArgumentMsg(name),
                        values.var: Utils.buildConstantArgumentMsg(value)
                    }, hasNext=i < dataset.shape[1])
                    
            #All Cells      
            else:
                col = 0
                while(col < dataset.shape[1]):
                    name = dataset.column_names[col]
                    row = 0
                    while(row < dataset.shape[0]): 
                        value = Utils.stringsConverter(tf.get_static_value(dataset[row][name]))
                        yield request.replySuccess({
                            row_index.var: Utils.buildConstantArgumentMsg(row),
                            column_index.var: Utils.buildConstantArgumentMsg(name),
                            values.var: Utils.buildConstantArgumentMsg(value)
                        }, hasNext = (row+1, col+1) != dataset.shape)
                        row += 1   
                    col +=1                        
                
        else:
            yield request.replyFail()
            
            
cellPrimitive = DistributedElements.DistributedPrimitiveWrapper("cell", 4, __CellPrimitive())