from dataqualitycheck.commonutilities import *
import polars as pl
try:
    import pyspark
    from pyspark.sql.functions import *
    from pyspark.sql.types import *
    from pyspark.context import SparkContext
    from pyspark.sql.session import SparkSession
    import pyarrow as pa
except:
    pass

class DatabricksSqlDF():
    def __init__(self):
        self.spark = SparkSession(SparkContext.getOrCreate())

    def read(self, source_input, no_of_partition = 4):
        try:
            df = self.spark.sql(f"select * from {source_input['source_name']}.{source_input['filename']}").repartition(no_of_partition)
        except Exception as e:
            raise Exception(f"Error occured while creating spark dataframe from {source_input['source_name']}.{source_input['filename']} , {e}")
        return df

    def read_enforce_schema_spark(self, source_input, schema, no_of_partition = 4):
        try:
            df = self.spark.sql(f"select * from {source_input['source_name']}.{source_input['filename']}").repartition(no_of_partition)
            df = self.spark.createDataFrame(df.collect(), schema=schema, verifySchema=False)
        except Exception as e:
            raise Exception(f"Error occured while creating enforce schema data from {source_input['source_name']}.{source_input['filename']}, {e}")
        return df
        
    def read_enforce_schema_polars(self, source_input,schema, no_of_partition = 4):
        try:
            polars_schema=[str(schema_val[1])  for schema_val in schema]
            columns=[schema_val[0] for  schema_val in schema]
            schema=eval(schema_enforce_structure(','.join(columns),','.join(polars_schema)))
            df = self.read_enforce_schema_spark(source_input, schema,no_of_partition )
            df = pl.from_arrow(pa.Table.from_batches(df._collect_as_arrow()))
        except Exception as e:
            raise Exception(f"Error occured while creating polars dataframe from {source_input['source_name']}.{source_input['filename']}, {e}")
        return df

    def read_into_polars(self, source_input, no_of_partition = 4 , infer_schema_in_polars = False):
        try:
            df = self.read(source_input, no_of_partition)
            df = pl.from_arrow(pa.Table.from_batches(df._collect_as_arrow()))
        except Exception as e:
            raise Exception(f"Error occured while creating polars dataframe from {source_input['source_name']}.{source_input['filename']}, {e}")
        return df

    def write(self, spark_df, database_name , table_name):
        try:
            self.spark.sql(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            table=table_name.replace('.','_').replace('::','_')
            spark_df.write.mode('append').saveAsTable(f"{database_name}.{table}")
        except Exception as e: 
            raise Exception(f"Error occured while writing spark data to {database_name}.{table} , {e}")
        return f"{database_name}.{table}"

    def write_from_polars(self, polar_df, database_name , table_name):
        try:
            polars_schema=[str(polar_df.schema[column]) for column in polar_df.columns]
            schema=eval(schema_enforce_structure(','.join(polar_df.columns),','.join(polars_schema)))
            df = self.spark.createDataFrame(polar_df.rows(), schema=schema)
            self.write(df, database_name , table_name)
        except Exception as e: 
            raise Exception(f"Error occured while writing polars data to {database_name}.{table_name} , {e}") 
        return f"{database_name}.{table_name}"
