import polars as pl
from datetime import date,datetime
from .enumfile import *
import time
try:
    import pyspark
    from pyspark.sql.functions import *
    from pyspark.sql.types import *
    from pyspark.context import SparkContext
    from pyspark.sql.session import SparkSession
except:
    pass

#----- Function to return tables list which is not present in given tables list.
def get_missing_tables(tables_list,rule_set):
    new_tables={}
    for rule in rule_set:
      source= f'''{rule["source_type"]}_{rule["layer"]}_{rule["source_name"]}_{rule["filename"]}'''
      if source not in tables_list.keys():
          new_tables[source]={"read_connector_method" : rule["read_connector_method"],
                                          "container_name": rule["container_name"],
                                          "latest_file_path": rule["latest_file_path"],
                                          "source_type": rule["source_type"],
                                          "layer":rule["layer"],
                                          "source_name": rule["source_name"],
                                          "filename": rule["filename"]
                                       }
    return new_tables
  
#----- Function to create a dictionary of dataframes from the tables passed in tables_list.
def read_dataset(tables_list, data_read_ob, no_of_partition, run_engine = 'pyspark', infer_schema_in_polars= False):
  d={}
  try:
    for table in tables_list.keys():
      if run_engine.lower() == 'polars' :
        d[table]= data_read_ob.read_into_polars(tables_list[table], no_of_partition , infer_schema_in_polars)
      else:
        d[table]= data_read_ob.read(tables_list[table], no_of_partition)
  except:
      raise Exception("Error occured while creating dataframe")
  return d

#------Function to create blob folder structures for different types of filepaths.
def get_folder_structure(rule, module_name):
    output_folder_structure = rule["output_folder_structure"]
    source_hirarchy = ''
    if rule["source_type"] and rule["source_type"] != 'null':
      source_hirarchy = f"{source_hirarchy}{rule['source_type']}/"
    if rule["source_name"] and rule["source_name"] != 'null':
      source_hirarchy = f"{source_hirarchy}{rule['source_name']}/"
    if rule["filename"] and rule["filename"] != 'null':
      source_hirarchy = f"{source_hirarchy}{rule['filename']}/"
    latest_file_path = rule["latest_file_path"]
    if latest_file_path.startswith(("abfss:", "dbfs:", "/dbfs", "https:")):
      if source_hirarchy in latest_file_path:
        latest_file_path = latest_file_path.split(source_hirarchy)[-1]
      elif rule["filename"] and rule["filename"] != 'null' and f"{rule['filename']}/" in latest_file_path:
        latest_file_path = latest_file_path.split(f"{rule['filename']}/")[-1]
      elif latest_file_path.startswith("abfss:"):
        latest_file_path = latest_file_path.split("windows.net/")[-1]
      elif latest_file_path.startswith("dbfs:"):
        latest_file_path = latest_file_path.lstrip('dbfs:/')
      elif latest_file_path.startswith("/dbfs"):
        latest_file_path = latest_file_path.lstrip('/dbfs/')
      elif latest_file_path.startswith("https:"):
        latest_file_path = latest_file_path.split("windows.net/")[-1].split('/', 1)[-1]
      folder_path = output_folder_structure + module_name + '/' + source_hirarchy + latest_file_path.rsplit('/', 1)[0]
    elif latest_file_path.startswith(("C:/" ,"D:/" ,"E:/","/home/")):
      initial_path = '/'.join(latest_file_path.split('/', 4)[:-1])
      if source_hirarchy in latest_file_path:
        latest_file_path = latest_file_path.split(source_hirarchy)[-1]
      elif rule["filename"] and rule["filename"] != 'null' and f"{rule['filename']}/" in latest_file_path:
        latest_file_path = latest_file_path.split(f"{rule['filename']}/")[-1]
      folder_path = initial_path + '/' + output_folder_structure + module_name + '/' + source_hirarchy + latest_file_path.split(initial_path)[-1].rsplit('/', 1)[0]
    else:
      folder_path = output_folder_structure + module_name+'/'+'databrickssql'+'/'+ source_hirarchy + latest_file_path.replace('.','_')
    if not folder_path.endswith('/'):
      folder_path = f"{folder_path}/"
    return folder_path
      
def config_cols_availability(infer_df, config_cols, source):
      list_cols_not_availabe = [col_name_config for col_name_config in config_cols.split(
          ',') if col_name_config not in infer_df.columns]
      if len(list_cols_not_availabe) > 0:
          raise Exception("missing columns")
          # raise SystemExit(f'''The cols {','.join(list_cols_not_availabe)} are present in config and not in the file {source}''')
  
#to get the schema
def schema_enforce_structure(col_name,value):
    value_list_mapped = [MappingDatatype.MAPPING_DATATYPE_DICT.value[value_key] for value_key in value.split(",")]
    combined_struct = tuple(zip(col_name.split(','),value_list_mapped))
    structure_list = [f'''StructField('{string_val[0]}',{string_val[1]},True)''' for string_val in combined_struct]
    enforce_schema = f"""StructType({str(structure_list).replace('''"''',"")})"""
    return enforce_schema
  
def schema_enforce_structure_polars(df,col_name,value):
    infered_schema_list=[df.schema[column] if column in df.columns else "" for column in col_name.split(',') ]
    combined_struct=tuple(zip(col_name.split(','),value.split(","),infered_schema_list))
    combined_struct=[string_val  for string_val in  combined_struct if string_val[0] in df.columns]
    enforce_schema= [tuple([string_val[0],string_val[2]]) if str(string_val[2]) in MappingDatatype.MAPPING_DATATYPE_DICT_POLARS.value[string_val[1]] else tuple([string_val[0], MappingDatatype.MAPPING_DATATYPE_DICT_POLARS.value[string_val[1]][-1]]) for string_val in combined_struct]
    return enforce_schema
     
# ----- Function to return failed record folder path
def get_failed_record_folder_path(rule, module_name, add_columns_in_folder_path=True):
    try:
      if add_columns_in_folder_path:
             column_names = rule["column_to_be_checked"].replace(',','__')
             folder_path = get_folder_structure(rule, module_name) + rule['rule_name'] + "/" + rule["column_to_be_checked"]+ "/"
      else:
             folder_path = get_folder_structure(rule, module_name) + rule['rule_name'] + "/" 
    except:
        raise Exception("Error occured while creating folder path")
    return folder_path
  
def get_failed_record_file_name(time_zone):
  return 'failed_records' + datetime.now(time_zone).strftime("_%d_%m_%Y_%H_%M_%S")
      
def get_schema(column_name, column_type, run_engine='pyspark'):
    if run_engine.lower() == 'polars':
        mapped_column_type_list = [MappingDatatype.MAPPING_DATATYPE_DICT_POLARS.value[value][-1] for value in column_type]
        schema = list(zip(column_name, mapped_column_type_list))

    else:
        mapped_column_type_list = [MappingDatatype.MAPPING_DATATYPE_DICT.value[value] for value in column_type]
        combined_struct = tuple(zip(column_name, mapped_column_type_list))
        structure_list = [f'''StructField('{string_val[0]}',{string_val[1]},True)''' for string_val in combined_struct]
        schema = eval(f"""StructType({str(structure_list).replace('''"''',"")})""")
    return schema

# ----- Function to define schema and create dataframe of the final result.
def data_check_summarization_spark_df(spark, test_summary):
    schema = get_schema(QualityCheckSummaryStructure.COLUMN_NAME.value, QualityCheckSummaryStructure.COLUMN_DATATYPE.value, 'pyspark')
    df = spark.createDataFrame(data=test_summary, schema=schema)
    return df
  
def data_quality_test_summary_tuple(job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start_time, run_date, modify_active = False, checked_columns = None):
    column_to_be_checked = checked_columns if checked_columns else rule["column_to_be_checked"]
    end_time = time.time()
    active = rule["active"] if 'active' in rule else 1
    active = 0 if modify_active else active
    time_taken = None if active == 0 else end_time - start_time
    result_data = (job_id, rule["container_name"], rule["source_type"], rule["layer"], rule["source_name"], rule["filename"], rule["read_connector_method"], rule["rule_name"], column_to_be_checked, rule['value'],
                    rule["ruletype"], active, test_status, total_row_count, failed_records_count, failed_records_write_location, time_taken, run_date)
    return result_data

def column_type_identifier(df, column_to_be_checked, run_engine =  'pyspark', n=1):
  if run_engine.lower() == 'polars':
    return column_type_identifier_polars(df, column_to_be_checked,n)
  else:
    return column_type_identifier_spark(df, column_to_be_checked,n)

def column_type_identifier_spark(df, column_to_be_checked, n=1):
        # For identifying numerical columns which are categorical.
        if (isinstance(df.schema[column_to_be_checked].dataType, (FloatType, IntegerType, LongType, ShortType, DoubleType)) and df.select(countDistinct(column_to_be_checked)).collect()[0][0] < n):
            column_type = ColumnType.CATEGORICAL.value
        # For identifying categorical columns.
        elif isinstance(df.schema[column_to_be_checked].dataType, (StringType, BooleanType)):
            column_type = ColumnType.CATEGORICAL.value
        # For identifying numerical Columns
        elif isinstance(df.schema[column_to_be_checked].dataType, (FloatType, IntegerType, LongType, ShortType, DoubleType)):
            column_type = ColumnType.NUMERICAL.value
        # For identifying date columns
        elif isinstance(df.schema[column_to_be_checked].dataType, (DateType, TimestampType)):
            column_type = ColumnType.DATE.value
        # Any other
        else:
            column_type = ColumnType.OTHER.value
        return column_type

def column_type_identifier_polars(df, column_to_be_checked, run_engine =  'pyspark', n=1):
        # For identifying numerical columns which are categorical.
        if ((df.schema[column_to_be_checked] in MappingDatatype.MAPPING_DATATYPE_DICT_POLARS.value["integer"] or df.schema[column_to_be_checked] in MappingDatatype.MAPPING_DATATYPE_DICT_POLARS.value["double"] or df.schema[column_to_be_checked] in MappingDatatype.MAPPING_DATATYPE_DICT_POLARS.value["float"]) and df.select(pl.col(column_to_be_checked).n_unique()).rows()[0][0] < n):
            column_type = ColumnType.CATEGORICAL.value
        # For identifying categorical columns.
        elif df.schema[column_to_be_checked] in MappingDatatype.MAPPING_DATATYPE_DICT_POLARS.value["string"] or df.schema[column_to_be_checked] in MappingDatatype.MAPPING_DATATYPE_DICT_POLARS.value["bool"]:
            column_type = ColumnType.CATEGORICAL.value
        # For identifying numerical Columns
        elif (df.schema[column_to_be_checked] in MappingDatatype.MAPPING_DATATYPE_DICT_POLARS.value["integer"] or df.schema[column_to_be_checked] in MappingDatatype.MAPPING_DATATYPE_DICT_POLARS.value["double"] or df.schema[column_to_be_checked] in MappingDatatype.MAPPING_DATATYPE_DICT_POLARS.value["float"]):
            column_type = ColumnType.NUMERICAL.value
        # For identifying date columns
        elif df.schema[column_to_be_checked] in MappingDatatype.MAPPING_DATATYPE_DICT_POLARS.value["date"]:
            column_type = ColumnType.DATE.value
        # Any other
        else:
            column_type = ColumnType.OTHER.value
        return column_type

def is_date_format_valid(date_str, date_format):
        try:
            if type(date_str) == "str":
                res = bool(datetime.strptime(date_str, date_format))
            else:
                date_str_new=str(date_str)
                res = bool(datetime.strptime(date_str_new, date_format))
                
        except Exception as e:
            res = False
            pass
        return res