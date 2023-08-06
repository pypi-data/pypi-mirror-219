# Databricks notebook source
import polars as pl
from enum import Enum

# COMMAND ----------

class QualityCheckSummaryStructure(Enum):
    COLUMN_NAME = ['job_id', 'container_name', 'source_type', 'layer', 'source_name',
                   'filename', 'read_connector_method','rule_name', 'column_to_be_checked',
                   'value', 'ruletype', 'active', 'status', 'total_row_count',
                   'failed_records_count', 'failed_records_write_location', 'time_taken', 'run_date']
    COLUMN_DATATYPE = ['string', 'string', 'string', 'string', 'string', 'string',
                       'string', 'string', 'string', 'string', 'string', 'string',
                       'string', 'string', 'string', 'string', 'float', 'string']
    
    
class ConsistencyCheckSummaryStructure(Enum):
    COLUMN_NAME = ['job_id', 'container_name', 'read_connector_method',
                   'base_table_source_type', 'base_table_layer',
                   'base_table_source_name', 'base_table_filename',
                   'base_table_sum', 'mapped_table_source_type',
                   'mapped_table_layer', 'mapped_table_source_name',
                   'mapped_table_filename', 'mapped_table_sum', 'description',
                   'difference', 'percentage_difference', 'run_date']
    COLUMN_DATATYPE = ['string', 'string', 'string', 'string', 'string', 'string',
                       'string', 'string', 'string', 'string', 'string', 'string',
                       'string', 'string', 'string', 'string', 'string']
    
    
class QualityCheckConfigStructure(Enum):
    COLUMN_NAME = ['container_name', 'source_type', 'layer', 'source_name', 'filename',
                   'read_connector_method', 'rule_name', 'column_to_be_checked', 'value',
                   'date_column_config', 'date_format_dictionary', 'ruletype', 'active',
                   'latest_file_path', 'output_folder_structure']
    COLUMN_DATATYPE = ['string', 'string', 'string', 'string', 'string', 'string',
                       'string', 'string', 'string', 'string', 'string', 'string',
                       'string', 'string', 'string']
    
class DataProfileReportStructure(Enum):
    COLUMN_NAME = ['job_id', 'source_type', 'layer', 'source_name', 'filename', 'column_name',
                   'column_type', 'total_column_count', 'total_row_count', 'min', 'max', 'avg',
                   'sum', 'stddev', '25th_per', '50th_per', '75th_per', 'missing_count',
                   'unique_count', 'mode', 'list_of_uniques', 'run_date']
    COLUMN_DATATYPE = ['string', 'string', 'string', 'string', 'string', 'string',
                       'string', 'string', 'string', 'string', 'string', 'string',
                       'string', 'string', 'string', 'string', 'string', 'string',
                       'string', 'string', 'string', 'string']

class ColumnType(Enum):
    NUMERICAL = 'NUMERICAL'
    CATEGORICAL = 'CATEGORICAL'
    DATE = 'DATE'
    OTHER = 'OTHER'
    
  
class MappingDatatype(Enum):
    MAPPING_DATATYPE_DICT = {'integer' : 'LongType()', 'int' : 'LongType()',
                             'long' : 'LongType()', 'str' : 'StringType()',
                             'string' : 'StringType()', 'double' : 'DoubleType()',
                             'float' : 'DoubleType()', 'date' : 'DateType()',
                             'bool': 'BooleanType()', 'Int64' : 'LongType()',
                             'Int32' : 'LongType()', 'Int16' : 'LongType()',
                             'Int8' : 'LongType()', 'Float64' : 'DoubleType()',
                             'Float32' : 'DoubleType()', 'UInt64' : 'LongType()',
                             'UInt32' : 'LongType()', 'UInt16' : 'LongType()',
                             'UInt8' : 'LongType()', 'Utf8' : 'StringType()',
                             'Date' : 'DateType()', 'Boolean' : 'BooleanType()'}
    MAPPING_DATATYPE_DICT_POLARS = {'integer' : ['Int8', 'Int16', 'Int32', 'Int64', 'UInt8',
                                                 'UInt16', 'UInt32', 'UInt64', pl.Int8, pl.Int16,
                                                 pl.Int32, pl.UInt8, pl.UInt16, pl.UInt32, pl.UInt64, pl.Int64],
                                    'int' : ['Int8', 'Int16', 'Int32', 'Int64', 'UInt8', 'UInt16',
                                             'UInt32', 'UInt64', pl.Int8, pl.Int16, pl.Int32, pl.UInt8,
                                             pl.UInt16, pl.UInt32, pl.UInt64, pl.Int64],
                                    'long' : ['Int8', 'Int16', 'Int32', 'Int64', 'UInt8', 'UInt16',
                                              'UInt32', 'UInt64', pl.Int8, pl.Int16, pl.Int32, pl.UInt8,
                                              pl.UInt16, pl.UInt32, pl.UInt64, pl.Int64],
                                    'str' : ['Utf8', 'Object', 'Categorical', pl.Utf8],
                                    'string' : ['Utf8', 'Object' , 'Categorical', pl.Utf8],
                                    'double' : ['Float32', 'Float64', pl.Float32, pl.Float64],
                                    'float' : ['Float32', 'Float64', pl.Float32, pl.Float64],
                                    'date' : ['Date',pl.Date], 'bool' : ["Boolean", pl.Boolean]}

class ModuleName(Enum):
    QUALITYCHECK = 'data_quality'
    DATAPROFILE = 'data_profiling'
    CONSISTENCYCHECK = 'consistency_check'



