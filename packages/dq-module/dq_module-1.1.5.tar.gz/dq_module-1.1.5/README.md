### dq-module
dq-module is a tool which can be used to perform validations and profiling on the datasets.This tool is compatible with two run_engines `pyspark` and `polars`.
### Features
## 1. Data Validation 
This library contains a `SingleDatasetQualityCheck()` class which can used to validate the dataset against a defined set of rules.
This class contains the following rules which can be used to validate the dataset: 
 - null_check
 - schema_check
 - range_min_check
 - range_max_check
 - length_check
 - unique_records_check
 - unique_keys_check
 - allowed_values_check
 - min_length_check
 - column_count_check
 - not_allowed_values_check
 -  date_range_check
 - regex_check
 - row_count_check

### How To Use

```sh
import dataqualitycheck as dq
from datetime import date
import time
```
##### Step 1: Adding a datasource
We have 4 classes which can be used to connect to a datasource:
1. `AzureBlobDF()` - This class can be used to interact with the datasources on azure blob storage . 
2. `DatabricksFileSystemDF()` - This class can be used to interect with the datasources on  databricks filesystem.
3. `DatabricksSqlDF()` - This class can be used to interact with the datasources on  databricks databases.
4. `LocalFileSystemDF()` - This class can be used to interact with the datasources on your local filesystem.

Each of the above class provides the functionalities to read and write from the respective datasources.


**Example:**
Pass the configuration of the  blob connector  in `blob_connector_config`and 
add a datasource by defining a `data_read_ob` and `data_write_ob`.
```sh
blob_connector_config = {"storage_account_name" : "rgmdemostorage", "container_name" : "cooler-images", "sas_token" : <vaild-sas-token>}
```
```sh
data_read_ob = dq.AzureBlobDF(storage_name=blob_connector_config["storage_account_name"], sas_token=blob_connector_config["sas_token"])
data_write_ob = dq.DatabricksFileSystemDF()
```

 `tables_list` is a dictionary that contains the list of sources along with the container_name , source_type , layer , source_name , filename , read_connector_method and latest_file_path  for the tables on which the validations has to be applied . 
```sh
#This is optional.It is required when you are calling individual rules.
tables_list = {}
```
##### Step 2: Add a DataContext 
Instantiate a DataContext by passing `tables_list`,`interaction_between_tables`,`data_read_ob`,`data_write_ob`, `data_right_structure`,`job_id`,`time_zone`,`no_of_partition` and `output_db_name `.
You can also pass the `run_engine` with which you want to apply the quality checks. By default, the run_engine is `pyspark`.

```sh
dq_ob = dq.SingleDatasetQualityCheck(tables_list={}, 
                                     interaction_between_tables=[],  
                                     data_read_ob=data_read_ob, 
                                     data_write_ob=data_write_ob, 
                                     data_right_structure='file',
                                     job_id=<pipeline_run_id>,
                                     time_zone=None,
                                     output_db_name=<database_name_where_report_has_to_be_written>,
                                     no_of_partition=4)
```

##### Step 3:
Passing a `rules_diagnosys_summery_file_path` and `config_df` as an input and apply validations on various columns of respective table defined in the `config_df`.

Here is an sample of the `config_df`.
| container_name   | source_type | layer     | source_name         | filename     | rule_name       | column_to_be_checked | value | date_column_config | date_format_dictionary | ruletype      | active | read_connector_method | latest_file_path                                                                                  | output_folder_structure | failed_schema_source_list |
|------------------|-------------|-----------|---------------------|--------------|-----------------|----------------------|-------|--------------------|------------------------|---------------|--------|-----------------------|---------------------------------------------------------------------------------------------------|-------------------------|---------------------------|
| rgm-data-quality | sharepoint  | processed | neilsen_data_folder | neilsen_data | null_check      | prod_brand           | null  | null               | null                   | Mandatory     | 1      | blob                  | path-to-file | processed/              |                           |
| rgm-data-quality | sharepoint  | processed | neilsen_data_folder | neilsen_data | range_min_check | inventory_kg_avg     | 10    | null               | null                   | Not Mandatory | 1      | blob                  | path-to-file | processed/              |                           |
| rgm-data-quality | sharepoint  | processed | neilsen_data_folder | neilsen_data | range_max_check | inventory_kg_avg     | 1000  | null               | null                   | Not Mandatory | 1      | blob                  | path-to-file | processed/              |                           |

**Example:**
```sh
rules_diagnosys_summery_folder_path = <folder-path-for-the-output-report>
 
config_df = spark.read.option("header",True).csv(<path-to-the-config>)

dq_ob.apply_validation(config_df, write_summary_on_database=True, failed_schema_source_list=[], output_summary_folder_path=rules_diagnosys_summery_folder_path)
```
## 2. Data Profiling
- We can generate a detailed summary statistics such as mean, median, mode, list of uniques, missing count etc. of a dataset using the `DataProfile()` class.
- This class can also be used to recommend some  data quality rules  based on the profiling report generated on the dataset.
### How To Use

**Step 1: Add a Datasource**
```sh
data_write_ob = dq.DatabricksSqlDF()
data_write_ob = dq.DatabricksSqlDF()
```
**Step 2: Add a DataContext**
```sh
import pytz
time_zone = pytz.timezone('US/Central')
dq_ob = dq.DataProfile(tables_list=tables_list,
                       interaction_between_tables=[],
                       data_read_ob=data_read_ob,
                       data_write_ob=data_write_ob,
                       data_right_structure='table',
                       job_id=<pipeline_run_id>,
                       time_zone=time_zone,
                       no_of_partition=4,
                       output_db_name=<database_name_where_report_has_to_be_written>,
                       run_engine='polars')
```
**Step 3:**
Pass `config_df` as an input and apply data profiling on various columns of respective table defined in the `config_df`.
``` sh
# You can create a config_df in pyspark/polars run_engine directly also rather than reading as a csv.
config_df = spark.createDataFrame([{"container_name" : "rgm-data-quality",
                                    "source_type" : "sharepoint",
                                    "layer" : "raw",
                                    "source_name" : "data_quality_db",
                                    "filename" : "neilsen_data_parquet",
                                    "latest_file_path" : "data_quality_db.neilsen_data_parquet",  
                                    "read_connector_method" : "databricks sql",
                                    "output_folder_structure" : "processed/data_profiling_test/"}])
```
```sh
# Generating a data profiling report.
dq_ob.apply_data_profiling(source_config_df=config_df,
                           write_consolidated_report=True)
```
```sh
# Generating a data profiling report as well as recommending the quality rules based on the profiling report.
rules_config = dq_ob.data_profiling_based_quality_rules(config_df, list_of_columns_to_be_ignored)
```

## 3. Consistency Check
 You can check the consistency of common columns between two tables using the `ConsistencyCheck()` class.
### How To Use

**Step 1: Add a datasource.**
```sh
data_read_ob = dq.DatabricksFileSystemDF()
data_write_ob = dq.AzureBlobDF(storage_name=blob_connector_config["storage_account_name"], sas_token=blob_connector_config["sas_token"])
```
**Step 2: Add a DataContext**
```sh
dq_ob = dq.ConsistencyCheck(tables_list={}, 
                            interaction_between_tables=[],
                            data_read_ob=data_read_ob,
                            data_write_ob=data_write_ob, 
                            data_right_structure='file',
                            job_id=<pipeline_run_id>,
                            time_zone=None,
                            no_of_partition=4,
                            output_db_name=<database_name_where_report_has_to_be_written>)
```
**Step 3:**
 Pass `config_df` and `output_report_folder_path` as an input and apply consistency check.
Here is a sample consistency check config.
| container_name   | base_table_source_type | base_table_layer | base_table_source_name | base_table_filename    | base_table_col_name | base_table_file_path                                                                                                | mapped_table_source_type | mapped_table_layer | mapped_table_source_name | mapped_table_filename    | mapped_table_col_name | mapped_table_file_path                                                                                                  | read_connector_method | output_folder_structure          |
|------------------|------------------------|------------------|------------------------|------------------------|---------------------|---------------------------------------------------------------------------------------------------------------------|--------------------------|--------------------|--------------------------|--------------------------|-----------------------|-------------------------------------------------------------------------------------------------------------------------|-----------------------|----------------------------------|
| rgm-data-quality | sharepoint             | processed        | scantrack              | butters_margarins_base | BARCODE             | dbfs:/FileStore/Tables/sharepoint/scantrack/butters_margarins_base/2023/01/12/butters_margarins_base_01_12_2023.csv | sharepoint               | processed          | scantrack                | butters_margarins_master | BARCODE               | dbfs:/FileStore/Tables/sharepoint/scantrack/butters_margarins_master/2023/01/12/butters_margarins_master_01_12_2023.csv | dbfs                  | processed/data_consistenct_test/ |
| rgm-data-quality | sharepoint             | processed        | scantrack              | cheese_base            | BARCODE             | dbfs:/FileStore/Tables/sharepoint/scantrack/cheese_base/2023/01/12/cheese_base_01_12_2023.csv                       | sharepoint               | processed          | scantrack                | cheese_master            | BARCODE               | dbfs:/FileStore/Tables/sharepoint/scantrack/cheese_master/2023/01/12/cheese_master_01_12_2023.csv                       | dbfs                  | processed/data_consistenct_test/ |


```sh
config_df = spark.read.option("header",True).csv(<path-to-the-consistency-check-config>)

output_report_folder_path = <folder-path-for-the-output-report>

dq_ob.apply_consistency_check(config_df, output_report_folder_path)

```


        
                          
                           