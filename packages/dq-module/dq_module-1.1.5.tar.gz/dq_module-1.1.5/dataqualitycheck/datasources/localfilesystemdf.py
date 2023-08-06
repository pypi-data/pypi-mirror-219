from .commonutilities import *
import os

class LocalFileSystemDF():
    def __init__(self):
        pass
    
    def read():
        raise Exception(f"read into spark not supported")

    def read_enforce_schema_spark(self, source_input, schema, no_of_partition = 4):
        raise Exception(f"read into spark not supported")
        
    def read_enforce_schema_polars(self, source_input,schema, no_of_partition = 4):
        filepath=source_input['latest_file_path']
        try:
            file_type = read_filetpye(filepath)
            df = read_file_into_enforce_polarsdf(file_type, filepath, schema, no_of_partition)
        except:
            raise Exception(f"Error occured while reading data from {filepath}")
        return df

    def read_into_polars(self,source_input,no_of_partition=4 , infer_schema_in_polars= False):
        filepath=source_input['latest_file_path']
        try:
            file_type = read_filetpye(filepath)
            df = read_file_into_polarsdf(file_type,filepath,no_of_partition ,infer_schema_in_polars)
        except:
            raise Exception(f"Error occured while reading data from {filepath}")
        return df
            
    def wirte():
        raise Exception(f"write into spark not supported")

    def write_from_polars(self,polar_df, save_output_folder_path, saved_file_new_name,rule=None):
        try:
            os.makedirs(f"{save_output_folder_path}",exist_ok=True)
            new_file_path = f"{save_output_folder_path}{saved_file_new_name}.csv"
            polar_df.write_csv(new_file_path)
        except:
            raise Exception(f"Error occured while writing polars data at {save_output_folder_path}")
        return new_file_path