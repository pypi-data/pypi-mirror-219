import polars as pl
try:
    import pyspark
    from pyspark.sql.functions import *
    from pyspark.sql.types import *
except:
    pass

def read_filetpye(source_path):
    filetype=source_path.split('.')[-1]
    if filetype.lower() == 'parquet':
        return 'parquet'
    elif filetype.lower() == 'csv':
        return 'csv'
    elif filetype.lower() == 'txt':
        return 'txt'
    else:
        raise Exception(f"unsupported filetype : {filetype}")

def read_file_into_enforce_sparkdf(spark, filetype, filepath, schema, no_of_partition):
    if filetype.lower() == 'parquet':
        df = spark.read.schema(schema).parquet(filepath).repartition(no_of_partition)            
    elif filetype.lower() == 'csv':
        df = spark.read.csv(filepath, schema=schema, header=True).repartition(no_of_partition) 
    elif filetype.lower() == 'txt':
        df = spark.read.csv(filepath, schema=schema, header=True, sep=",").repartition(no_of_partition)
    else:
        raise Exception(f"spark dataframe not created using {filepath}") 
    return df
    
def read_file_into_enforce_polarsdf(filetype,file_path,schema,no_of_partition):                                                     
    if filetype.lower() == 'parquet':
        df= pl.read_parquet(file_path)
    
    elif filetype.lower() == 'csv':
        dtypes=[schema_val[1] for schema_val in schema]
        df = pl.read_csv(file_path,dtypes=dtypes,ignore_errors=True)
    else :
        raise Exception(f"polar dataframe not created using {filepath}") 
    return df
    
def read_file_into_sparkdf(spark, filetype, filepath, no_of_partition):
    if filetype.lower() == 'parquet':
        df = spark.read.option("header", "true").option("inferSchema", "true").format("parquet").load(filepath).repartition(no_of_partition)            
    elif filetype.lower() == 'csv':
        df = spark.read.option("header",True).option("inferSchema", "true").format("csv").load(filepath).repartition(no_of_partition)
    elif filetype.lower() == 'txt':
        df = spark.read.option("header", "true").option("delimiter", ",").option("inferSchema", "true").format("csv").load(filepath).repartition(no_of_partition)
    else:
        raise Exception(f"spark dataframe not created using {filepath}") 
    return df
  
def read_file_into_polarsdf(filetype,file_path, no_of_partition , infer_schema_in_polars = False):                                                     
    if filetype.lower() == 'parquet':
        df= pl.read_parquet(file_path)
        
    elif filetype.lower() == 'csv':
       if infer_schema_in_polars == True:
        df = pl.read_csv(file_path,encoding='utf8-lossy')
       else:
        df = pl.read_csv(file_path,infer_schema_length=0,encoding='utf8-lossy')
    else :
        raise Exception(f"polar dataframe not created using {filepath}") 
    return df