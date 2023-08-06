from .commonutilities import *
try:
    import pyspark
    from pyspark.sql.functions import *
    from pyspark.sql.types import *
    from pyspark.context import SparkContext
    from pyspark.sql.session import SparkSession
except:
    pass

class DatabricksFileSystemDF():
    def __init__(self):
        self.spark = SparkSession(SparkContext.getOrCreate())

    def read(self, source_input, no_of_partition = 4):
        try:
            source_path = source_input['latest_file_path']
            if source_path.startswith("dbfs:"):
                pass
            else:
                source_path = f"dbfs:{source_path}"
            file_type = read_filetpye(source_path)
            df = read_file_into_sparkdf(self.spark, file_type, source_path, no_of_partition)
        except:
            raise Exception(f"Error occured while creating spark dataframe using {source_path}, {e}")
        return df

    def read_enforce_schema_spark(self, source_input, schema, no_of_partition = 4):
        try:
            source_path = source_input['latest_file_path']
            if source_path.startswith("dbfs:"):
                pass
            else:
                source_path = f"dbfs:{source_path}"
                
            file_type = read_filetpye(source_path)
            df = read_file_into_enforce_sparkdf(self.spark, file_type, source_path, schema, no_of_partition)
        except Exception as e:
            raise Exception(f"Error occured while reading data from {source_path}, {e}")
        return df
    
    def  read_enforce_schema_polars(self, source_input,schema, no_of_partition = 4):
        try:
            source_path = source_input['latest_file_path']
            if source_path.startswith("/dbfs"):
                pass
            elif source_path.startswith("dbfs:"):
                source_path = source_path.replace('dbfs:','/dbfs')
            else:
                source_path = f"/dbfs/{source_path}"

            file_type = read_filetpye(source_path)
            df = read_file_into_enforce_polarsdf(file_type, source_path,schema, no_of_partition)
        except:
            raise Exception(f"Error occured while reading data from {source_path}, {e}")
        return df

    def read_into_polars(self, source_input, no_of_partition = 4 ,infer_schema_in_polars = False):
        try:
            source_path = source_input['latest_file_path']
            if source_path.startswith("/dbfs"):
                pass
            elif source_path.startswith("dbfs:"):
                source_path = source_path.replace('dbfs:','/dbfs')
            else:
                source_path = f"/dbfs/{source_path}"

            file_type = read_filetpye(source_path)
            df = read_file_into_polarsdf(file_type, source_path, no_of_partition , infer_schema_in_polars)
        except:
            raise Exception(f"Error occured while reading data from {source_path}, {e}")
        return df

    def write(self, spark_df, save_output_folder_path , saved_file_new_name, rule=None):
        from pyspark.dbutils import DBUtils
        try:
            spark_df.coalesce(1).write.mode("append").csv(save_output_folder_path, header = True)
            # getting the file paths at the given saved file location
            output_file_path = []
            delete_file_path = []
            dbutils = DBUtils(self.spark)
            for file_path in dbutils.fs.ls(save_output_folder_path):
                if 'part-' in file_path.name:
                    output_file_path.append(file_path.path)
                elif '.csv' in file_path.name:
                    pass
                elif len(dbutils.fs.ls(file_path.path)) > 1:
                    pass
                elif file_path.path.endswith('/'):
                    pass
                else:
                    delete_file_path.append(file_path.path)

            #saving the file with the proper name 
            new_file_path = output_file_path[-1]
            new_file_folder_path = '/'.join(output_file_path[0].split('/')[:-1])
            new_file_name = f"{saved_file_new_name}.csv"
            new_file_path = new_file_folder_path+'/'+new_file_name
            dbutils.fs.mv(output_file_path[0],new_file_path)
            #removing the unnecessary files
            for delete_path in delete_file_path:
                try:
                    if dbutils.fs.ls(delete_path):
                        dbutils.fs.rm(delete_path)
                except:
                    pass
        except Exception as e: 
            raise Exception(f"Error occured while writing spark data at {save_output_folder_path} , {e}") 
        return new_file_path

    def write_from_polars(self,polar_df,save_output_folder_path, saved_file_new_name,rule=None):
        from pyspark.dbutils import DBUtils              
        try:
            dbutils = DBUtils(self.spark)
            dbutils.fs.mkdirs(save_output_folder_path)
            if save_output_folder_path.startswith("dbfs:"):
               save_output_folder_path =save_output_folder_path.replace('dbfs:','/dbfs')
            elif save_output_folder_path.startswith("/dbfs"):
               pass
            else:
               save_output_folder_path=f"/dbfs/{save_output_folder_path}"
            

            new_file_path = f"{save_output_folder_path}{saved_file_new_name}.csv"
            polar_df.write_csv(new_file_path)
        except Exception as e:
            raise Exception(f"Error occured while writing polars data at {save_output_folder_path}, {e}")
        return new_file_path
