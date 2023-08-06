from datetime import date,datetime
import time
from .commonutilities import *
from itertools import zip_longest
import polars as pl
from .datasources.databrickssqldf import DatabricksSqlDF
from dateutil.parser import parse
try:
    import pyspark
    from pyspark.sql.functions import *
    from pyspark.sql.types import *
    from pyspark.context import SparkContext
    from pyspark.sql.session import SparkSession
except:
    pass


class SingleDatasetQualityCheckPolars():
    def __init__(self, tables_list, interaction_between_tables, data_read_ob, data_write_ob, data_right_structure, job_id, time_zone=None, output_db_name="data_quality_output", no_of_partition=4):
        # self.spark = SparkSession(SparkContext.getOrCreate())
        self.tables_list = tables_list
        self.interaction_between_tables = interaction_between_tables
        self.test_summary = []
        self.no_of_partition = no_of_partition
        self.data_read_ob = data_read_ob
        self.data_write_ob = data_write_ob
        self.run_engine = 'polars'
        self.dataframes = read_dataset(
            self.tables_list, self.data_read_ob, self.no_of_partition, self.run_engine)
        self.output_db_name = output_db_name
        self.job_id = job_id
        self.data_right_structure = data_right_structure
        self.time_zone = time_zone
        

    # ----- Function to define schema and create dataframe of the final result.

    def data_check_summarization(self, test_summary):
        schema = get_schema(QualityCheckSummaryStructure.COLUMN_NAME.value, QualityCheckSummaryStructure.COLUMN_DATATYPE.value, self.run_engine)
        df = pl.DataFrame(data=test_summary, schema=schema)
        return df

    def write_failed_records(self, rule, failed_df, write_failed_records_flag=True, add_columns_in_folder_path=True):
        if 'write_failed_records' in rule and rule['write_failed_records'] == 'False':
            failed_records_write_location = 'Failed records are not written.'

        elif write_failed_records_flag == False:
            failed_records_write_location = 'Failed records are not written.'
            
        else:
            if self.data_right_structure == 'file':
                failed_record_folder_path = get_failed_record_folder_path(
                    rule, ModuleName.QUALITYCHECK.value, add_columns_in_folder_path)
                failed_record_file_name = get_failed_record_file_name(self.time_zone)
                failed_records_write_location = self.data_write_ob.write_from_polars(
                    failed_df, failed_record_folder_path, failed_record_file_name, rule)
            else:
                table_name = f'''{rule["source_type"]}_{rule["layer"]}_{rule["source_name"]}_{rule["filename"]}'''
                failed_records_write_location = self.data_write_ob.write_from_polars(
                    failed_df, self.output_db_name, table_name)
        return failed_records_write_location

    def drift_report(self, config_col, dataframe_col):
        # indivisual data drift reports
        drift_df = pl.DataFrame(zip_longest(config_col.split(
            ','), dataframe_col), schema=['config_cols', 'dataframe_cols'])
        return drift_df.with_columns(pl.when((pl.col('config_cols') == pl.col('dataframe_cols')) & (pl.col('config_cols').is_not_null())).then(("No Drift")).otherwise(("Drift")).alias("Drift"))

    def date_format_function(self, infer_df, date_col_names, date_col_format, column_names, date_format_dictionary=None):
        try:
            total_records_rows = []
            exception_msg = ''
            date_format_dictionary = eval(date_format_dictionary) if date_format_dictionary and date_format_dictionary != 'null' else {}
            for date_column_name in date_col_names:
                date_format = date_col_format[date_column_name]
                try:
                    if date_format_dictionary and date_format in date_format_dictionary:
                        date_format = date_format_dictionary[date_format]
                    else:
                        exception_msg = f"{date_format} Date format is not present in dictionary."
                        raise Exception(exception_msg)
                except Exception as e:
                    exception_msg =  exception_msg if e.args[0] == exception_msg else "Date format dictionary is not present."
                    raise Exception(exception_msg)
                if infer_df.schema[date_column_name]== pl.Utf8:
                  failed_records = infer_df.with_columns(pl.when(pl.col(date_column_name).str.strptime(pl.Date, date_format, strict=False).is_not_null()).then(True).otherwise(False).alias(f"{date_column_name}_bad_record")).\
                    filter(pl.col(f"{date_column_name}_bad_record") == False).\
                    drop(f"{date_column_name}_bad_record").rows(
                )  # will return true in case the data is in the prescribed format or else will give as bad records
                  total_records_rows.extend(failed_records)
                else:
                   failed_records = infer_df.with_columns(pl.when(pl.col(date_column_name).cast(pl.Utf8).str.strptime(pl.Date, date_format, strict=False).is_not_null()).then(True).otherwise(False).alias(f"{date_column_name}_bad_record")).\
                    filter(pl.col(f"{date_column_name}_bad_record") == False).\
                    drop(f"{date_column_name}_bad_record").rows()
                   total_records_rows.extend(failed_records)

            total_records_df = pl.DataFrame(total_records_rows, schema=schema_enforce_structure_polars(
                infer_df, 'row_nr,'+column_names, 'int,'+",".join(['str']*len(column_names.split(',')))))
            total_records_df = total_records_df.unique(subset=total_records_df.columns)
        except Exception as e:
            raise Exception(e)
        return total_records_df
    # ----- Function to check if column have any null value.

    def null_check(self, df, rule, write_failed_records_flag):
        start = time.time()
        run_date = date.today().strftime("%Y/%m/%d")
        total_row_count = df.height
        result = df.filter(pl.col(rule["column_to_be_checked"]).is_null())
        #result = df.filter(~pl.all(pl.col(rule["column_to_be_checked"]).is_not_null()))
        failed_records_count = result.height
        failed_records_write_location = 'N/A'
        if failed_records_count == 0:
            test_status = "PASS"
        else:
            test_status = "FAIL"
            failed_df = result.with_columns(
                [
                    pl.lit(run_date).alias("Run_Date"),
                    pl.lit(rule["rule_name"]).alias("Rule"),
                    pl.lit(f"{rule['column_to_be_checked']}:{rule['value']}").alias(
                        "Column_Tested"),
                    pl.lit(1 if rule["ruletype"] ==
                           'Mandatory' else 0).alias("Mandatory"),
                    pl.lit(self.job_id).alias("job_id")
                ]
            )
            failed_records_write_location = self.write_failed_records(
                rule, failed_df,  write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

    def schema_check(self, df, rule,  write_failed_records_flag):
        run_date = date.today().strftime("%Y/%m/%d")
        start = time.time()
        date_col_config = eval(
            rule["date_column_config"]) if rule["date_column_config"] and rule["date_column_config"] != 'null' else {}
        total_row_count = df.height
        failed_records_count = 0
        failed_records_write_location = 'N/A'
        reason = ''
        col_list = rule["column_to_be_checked"].split(',')
        value_list = rule["value"].split(',')
        try:
            # check if the config cols actually present or not
            config_cols_availability(
                df, rule["column_to_be_checked"], rule["layer"])

            if len(col_list) != len(value_list):
                raise Exception("missing column datatypes")
            if len(col_list) != len(df.columns):
                raise Exception("extra column found")
            if rule["column_to_be_checked"] != ",".join(df.columns):
                raise Exception("column sequence mismatched")

            # getting the cols only in the col name column in config
            infer_df_config = df.select(
                rule["column_to_be_checked"].split(','))
            infer_df_config_cols = infer_df_config.with_row_count()
            # date cols ka validation ke liye
            date_col_names = [col_list[data_index] for data_index in range(
                len(value_list)) if 'date' in str(value_list[data_index]).lower()]

            # check requirements to run the date check function or not
            failed_date_records_count = 0
            failed_date_records = pl.DataFrame([], schema=schema_enforce_structure_polars(df,
                                                                                           rule["column_to_be_checked"], rule["value"])).with_row_count()
            if len(date_col_names) > 0:
                failed_date_records = self.date_format_function(
                    infer_df_config_cols, date_col_names, date_col_config, rule["column_to_be_checked"], rule["date_format_dictionary"])
                failed_date_records_count = failed_date_records.height

            # non date cols schema checkups
            non_date_cols = ','.join(
                [column for column in infer_df_config_cols.columns if column not in date_col_names])
            infer_df_selected_cols = infer_df_config_cols.select(
                non_date_cols.split(','))  # non date cols only
            schema_enforce=schema_enforce_structure_polars(
                df,   rule["column_to_be_checked"], rule["value"])
            enforce_df_selected_cols = self.data_read_ob.read_enforce_schema_polars(rule, schema_enforce, self.no_of_partition).with_row_count().select(
                non_date_cols.split(','))
            infer_df_selected_cols1=infer_df_selected_cols.fill_null("0").fill_null(0).with_columns(  [pl.concat_str(infer_df_selected_cols.fill_null("0").fill_null(0).columns,    sep="//").alias("concat_cols"),])
            enforce_df_selected_cols1=enforce_df_selected_cols.fill_null("0").fill_null(0).with_columns(  [pl.concat_str(enforce_df_selected_cols.fill_null("0").fill_null(0).columns,    sep="//" ).alias("concat_cols"),])    
            failed_enforce_records1 = infer_df_selected_cols1.join(enforce_df_selected_cols1 , on=["concat_cols"] , how="anti")        
            failed_enforce_records=infer_df_selected_cols.join(failed_enforce_records1 , on=["row_nr"] , how="inner").select(infer_df_selected_cols.columns)      
            failed_enforce_records_count = failed_enforce_records.height
            
            test_status = "PASS" if failed_enforce_records.height == 0 and failed_date_records_count == 0 else "FAIL"
            # if test_status == "Pass":
            #     if infer_df_selected_cols.dtypes != enforce_df_selected_cols.dtypes:
            #         raise Exception('schema is different.')
            # else:
            if test_status == "FAIL":
                failed_records_count = failed_date_records_count + failed_enforce_records_count
                if failed_date_records_count != 0 and failed_enforce_records_count != 0:
                    failed_enforce_records_cols=failed_enforce_records.columns
                    failed_df = failed_date_records.join(
                        failed_enforce_records, on=failed_enforce_records_cols, how='outer').drop('row_nr')
                    reason = ', invalid data type and date format'
                elif failed_date_records_count != 0:
                    failed_df = failed_date_records.drop('row_nr')
                    reason = ', invalid date format'
                else:
                    failed_df = failed_enforce_records.drop('row_nr')
                    reason = ', invalid data type'

                failed_df = failed_df.with_columns(
                    [
                        pl.lit(run_date).alias("Run_Date"),
                        pl.lit(rule["rule_name"]).alias("Rule"),
                        pl.lit("All columns").alias("Column_Tested"),
                        pl.lit(1 if rule["ruletype"] ==
                               'Mandatory' else 0).alias("Mandatory"),
                        pl.lit(self.job_id).alias("job_id")
                    ]
                )
                failed_records_write_location = self.write_failed_records(
                    rule, failed_df, write_failed_records_flag, False)

        except Exception as e:
            test_status = "FAIL"
            failed_records_count = total_row_count
            reason = f', {e}'
            failed_df = df.with_columns(
                [
                    pl.lit(run_date).alias("Run_Date"),
                    pl.lit(rule["rule_name"]).alias("Rule"),
                    pl.lit("All columns").alias("Column_Tested"),
                    pl.lit(1 if rule["ruletype"] ==
                           'Mandatory' else 0).alias("Mandatory"),
                    pl.lit(self.job_id).alias("job_id")
                ]
            )
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag, False)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status + reason, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

    # ----- Function to check if values not be less than the given value

    def range_min_check(self, df, rule, write_failed_records_flag):
        start = time.time()
        run_date = date.today().strftime("%Y/%m/%d")
        total_row_count = df.height
#         df = df.filter(~pl.all(pl.col(rule["column_to_be_checked"]).is_null()))
        result = df.filter(pl.col(rule["column_to_be_checked"]).cast(
            pl.Float64, strict=False) < float(rule["value"]))
        failed_records_count = result.height
        failed_records_write_location = 'N/A'
        if failed_records_count == 0:
            test_status = "PASS"
        else:
            test_status = "FAIL"
            failed_df = result.with_columns(
                [
                    pl.lit(run_date).alias("Run_Date"),
                    pl.lit(rule["rule_name"]).alias("Rule"),
                    pl.lit(f"{rule['column_to_be_checked']}:{rule['value']}").alias(
                        "Column_Tested"),
                    pl.lit(1 if rule["ruletype"] ==
                           'Mandatory' else 0).alias("Mandatory"),
                    pl.lit(self.job_id).alias("job_id")
                ]
            )
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag)
        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

    # ----- Function to check if values should not be less than or equal to the required value
#    def range_min_inclusive_check(self, df, rule, write_failed_records_flag):
#       start = time.time()
#        run_date = date.today().strftime("%Y/%m/%d")
#        total_row_count = df.height
#         df = df.filter(~pl.all(pl.col(rule["column_to_be_checked"]).is_null()))
#        result = df.filter(
#            pl.col(rule["column_to_be_checked"]).cast(pl.Float64, strict=False) <= float(rule["value"]))
#        failed_records_count = result.height
#        failed_records_write_location = 'N/A'
#        if failed_records_count == 0:
#            test_status = "PASS"
#        else:
#            test_status = "FAIL"
#            failed_df = result.with_columns(
#                [
#                    pl.lit(run_date).alias("Run_Date"),
#                    pl.lit(rule["rule_name"]).alias("Rule"),
#                    pl.lit(f"{rule['column_to_be_checked']}:{rule['value']}").alias(
#                        "Column_Tested"),
#                    pl.lit(1 if rule["ruletype"] ==
#                           'Mandatory' else 0).alias("Mandatory"),
#                    pl.lit(self.job_id).alias("job_id")
#                ]
#            )
#            failed_records_write_location = self.write_failed_records(
#                rule, failed_df, write_failed_records_flag)
#
#        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

    # ----- Function to check if values should not be greater then the given value
    def range_max_check(self, df, rule, write_failed_records_flag):
        start = time.time()
        run_date = date.today().strftime("%Y/%m/%d")
        total_row_count = df.height
#         df = df.filter(~pl.all(pl.col(rule["column_to_be_checked"]).is_null()))
        result = df.filter(
            pl.col(rule["column_to_be_checked"]).cast(pl.Float64, strict=False) > float(rule["value"]))
        failed_records_count = result.height
        failed_records_write_location = 'N/A'
        if failed_records_count == 0:
            test_status = "PASS"
        else:
            test_status = "FAIL"
            failed_df = result.with_columns(
                [
                    pl.lit(run_date).alias("Run_Date"),
                    pl.lit(rule["rule_name"]).alias("Rule"),
                    pl.lit(f"{rule['column_to_be_checked']}:{rule['value']}").alias(
                        "Column_Tested"),
                    pl.lit(1 if rule["ruletype"] ==
                           'Mandatory' else 0).alias("Mandatory"),
                    pl.lit(self.job_id).alias("job_id")
                ]
            )
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

    # ----- Function to check if the values in the column have given length or not.
    def length_check(self, df, rule, write_failed_records_flag):
        start = time.time()
        run_date = date.today().strftime("%Y/%m/%d")
        total_row_count = df.height
        result = df.filter(
            pl.col(rule["column_to_be_checked"]).cast(pl.Utf8,strict=False).str.lengths() > int(rule["value"]))
        failed_records_count = result.height
        failed_records_write_location = 'N/A'
        if failed_records_count == 0:
            test_status = "PASS"
        else:
            test_status = "FAIL"
            failed_df = result.with_columns(
                [
                    pl.lit(run_date).alias("Run_Date"),
                    pl.lit(rule["rule_name"]).alias("Rule"),
                    pl.lit(f"{rule['column_to_be_checked']}:{rule['value']}").alias(
                        "Column_Tested"),
                    pl.lit(1 if rule["ruletype"] ==
                           'Mandatory' else 0).alias("Mandatory"),
                    pl.lit(self.job_id).alias("job_id")
                ]
            )
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

    # ----- Function to check if all the records are unique or not in the table.
    def unique_records_check(self, df, rule, write_failed_records_flag):
        start = time.time()
        run_date = date.today().strftime("%Y/%m/%d")
        total_row_count = df.height
        columnList = df.columns
        d = df.select(columnList)
        result = df.filter(pl.lit(d.is_duplicated()))
        failed_records_count = result.height
        failed_records_write_location = 'N/A'
        if failed_records_count == 0:
            test_status = "PASS"
        else:
            test_status = "FAIL"
            failed_df = result.with_columns(
                [
                    pl.lit(run_date).alias("Run_Date"),
                    pl.lit(rule["rule_name"]).alias("Rule"),
                    pl.lit("All columns").alias(
                        "Column_Tested"),
                    pl.lit(1 if rule["ruletype"] ==
                           'Mandatory' else 0).alias("Mandatory"),
                    pl.lit(self.job_id).alias("job_id")
                ]
            )

            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag, False)
        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date, False, ",".join(df.columns))

    # ----- Function to check if all the records are unique for all given input columns.It takes a list of columns as an arguement

    def unique_keys_check(self, df, rule, write_failed_records_flag):
        start = time.time()
        run_date = date.today().strftime("%Y/%m/%d")
        total_row_count = df.height
        d = df.select(list(rule["column_to_be_checked"].split(",")))
        result = df.filter(pl.lit(d.is_duplicated()))
        failed_records_count = result.height
        failed_records_write_location = 'N/A'
        if failed_records_count == 0:
            test_status = "PASS"
        else:
            test_status = "FAIL"
            failed_df = result.with_columns(
                [
                    pl.lit(run_date).alias("Run_Date"),
                    pl.lit(rule["rule_name"]).alias("Rule"),
                    pl.lit(f"{rule['column_to_be_checked']}:{rule['value']}").alias(
                        "Column_Tested"),
                    pl.lit(1 if rule["ruletype"] ==
                           'Mandatory' else 0).alias("Mandatory"),
                    pl.lit(self.job_id).alias("job_id")
                ]
            )
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

    # ----- Function takes a list of allowed values for a particular column and check if the values of the column belongs to that list or not.
    def allowed_values_check(self, df, rule, write_failed_records_flag):
        start = time.time()
        run_date = date.today().strftime("%Y/%m/%d")
        total_row_count = df.height
        result = df.filter(
            pl.col(rule["column_to_be_checked"]).is_in(rule["value"].strip().split(',')).is_not())
        failed_records_count = result.height
        failed_records_write_location = 'N/A'
        if failed_records_count == 0:
            test_status = "PASS"
        else:
            test_status = "FAIL"
            failed_df = result.with_columns(
                [
                    pl.lit(run_date).alias("Run_Date"),
                    pl.lit(rule["rule_name"]).alias("Rule"),
                    pl.lit(f"{rule['column_to_be_checked']}:{rule['value']}").alias(
                        "Column_Tested"),
                    pl.lit(1 if rule["ruletype"] ==
                           'Mandatory' else 0).alias("Mandatory"),
                    pl.lit(self.job_id).alias("job_id")
                ]
            )
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

    # ----- Function to check that if the values in the column has the required minimum length or not.
    def min_length_check(self, df, rule, write_failed_records_flag):
        start = time.time()
        run_date = date.today().strftime("%Y/%m/%d")
        total_row_count = df.height
        result = df.filter(
            pl.col(rule["column_to_be_checked"]).cast(pl.Utf8,strict=False).str.lengths() < int(rule["value"]))
        failed_records_count = result.height
        failed_records_write_location = 'N/A'
        if failed_records_count == 0:
            test_status = "PASS"
        else:
            test_status = "FAIL"
            failed_df = result.with_columns(
                [
                    pl.lit(run_date).alias("Run_Date"),
                    pl.lit(rule["rule_name"]).alias("Rule"),
                    pl.lit(f"{rule['column_to_be_checked']}:{rule['value']}").alias(
                        "Column_Tested"),
                    pl.lit(1 if rule["ruletype"] ==
                           'Mandatory' else 0).alias("Mandatory"),
                    pl.lit(self.job_id).alias("job_id")
                ]
            )
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag)
        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

    # ----- Function to check that the table has required column count or not.
    def column_count_check(self, df, rule, write_failed_records_flag):
        start = time.time()
        run_date = date.today().strftime("%Y/%m/%d")
        total_row_count = df.height
        total_col_count = len(df.columns)
        failed_records_count = total_col_count - int(rule["value"])
        failed_records_write_location = 'N/A'
        if total_col_count == int(rule["value"]):
            test_status = "PASS"
        else:
            test_status = "FAIL"
            result = pl.DataFrame(
                data=[tuple([None for x in df.columns])], schema=df.schema)
            failed_df = result.with_columns(
                [
                    pl.lit(run_date).alias("Run_Date"),
                    pl.lit(rule["rule_name"]).alias("Rule"),
                    pl.lit(f"{rule['column_to_be_checked']}:{rule['value']}").alias(
                        "Column_Tested"),
                    pl.lit(1 if rule["ruletype"] ==
                           'Mandatory' else 0).alias("Mandatory"),
                    pl.lit(self.job_id).alias("job_id")
                ]
            )
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag, False)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

    # ----- Function takes a list of not allowed values for a particular column and check if the column has not allowed values or not.
    def not_allowed_values_check(self, df, rule, write_failed_records_flag):
        start = time.time()
        run_date = date.today().strftime("%Y/%m/%d")
        total_row_count = df.height
        result = df.filter(
            pl.col(rule["column_to_be_checked"]).is_in(rule["value"].strip().split(',')))
        failed_records_count = result.height
        failed_records_write_location = 'N/A'
        if failed_records_count == 0:
            test_status = "PASS"
        else:
            test_status = "FAIL"
            failed_df = result.with_columns(
                [
                    pl.lit(run_date).alias("Run_Date"),
                    pl.lit(rule["rule_name"]).alias("Rule"),
                    pl.lit(f"{rule['column_to_be_checked']}:{rule['value']}").alias(
                        "Column_Tested"),
                    pl.lit(1 if rule["ruletype"] ==
                           'Mandatory' else 0).alias("Mandatory"),
                    pl.lit(self.job_id).alias("job_id")
                ]
            )
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

    # ----- Function to check if the date lies in the given range or not.
    def date_range_check(self, df, rule, write_failed_records_flag):
        start = time.time()
        run_date = date.today().strftime("%Y/%m/%d")
        total_row_count = df.height
        value = eval(rule["value"])
        
        min_value= parse( value["min_value"] )
        max_value= parse( value["max_value"] )
        date_column_config = eval(rule["date_column_config"])
        date_format_dictionary= eval( rule["date_format_dictionary"] )
        date_format = date_format_dictionary[date_column_config[rule['column_to_be_checked']]]
        try:
          if df.schema[rule['column_to_be_checked']]== pl.Utf8:
            df1= df.with_columns([pl.col(rule['column_to_be_checked']).str.strptime(pl.Date,date_format).alias("new_date")])
            result = df1.filter(~pl.col("new_date").is_between(min_value,max_value, 'both')).drop("new_date")
          else:
           if datetime.strftime(df[0,rule['column_to_be_checked']], "%Y-%m-%d")== str(df[0,rule['column_to_be_checked']]):
             result = df.filter(~pl.col(rule["column_to_be_checked"]).is_between(min_value,max_value))
           else:
             df1= df.with_columns([pl.col(rule['column_to_be_checked']).dt.strftime("%Y-%m-%d").str.strptime(pl.Date,"%Y-%m-%d", strict=False).alias("new_date")])
             result = df1.filter(~pl.col("new_date").is_between(min_value,max_value, 'both')).drop("new_date")

          failed_records_count = result.height
          failed_records_write_location = 'N/A'
          if failed_records_count == 0:
            test_status = "PASS"
          else:
            test_status = "FAIL"
            failed_df = result.with_columns(
                [
                    pl.lit(run_date).alias("Run_Date"),
                    pl.lit(rule["rule_name"]).alias("Rule"),
                    pl.lit(f"{rule['column_to_be_checked']}:{rule['value']}").alias(
                        "Column_Tested"),
                    pl.lit(1 if rule["ruletype"] ==
                           'Mandatory' else 0).alias("Mandatory"),
                    pl.lit(self.job_id).alias("job_id")
                ]
            )
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag)
        except :
          raise Exception("Wrong date format in date column config")
            
        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

    # ----- Function to check if the given column matches the given regex pattern or not.
    def regex_check(self, df, rule, write_failed_records_flag):
        start = time.time()
        run_date = date.today().strftime("%Y/%m/%d")
        total_row_count = df.height
        result = df.filter(
            pl.col(rule["column_to_be_checked"]).str.contains(rule["value"]).is_not())
        failed_records_count = result.height
        failed_records_write_location = 'N/A'
        test_status = "PASS" if failed_records_count == 0 else "FAIL"

        if failed_records_count > 0:
            failed_df = result.with_columns(
                [
                    pl.lit(run_date).alias("Run_Date"),
                    pl.lit(rule["rule_name"]).alias("Rule"),
                    pl.lit(f"{rule['column_to_be_checked']}:{rule['value']}").alias(
                        "Column_Tested"),
                    pl.lit(1 if rule["ruletype"] ==
                           'Mandatory' else 0).alias("Mandatory"),
                    pl.lit(self.job_id).alias("job_id")
                ]
            )
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

    def row_count_check(self, df, rule, write_failed_records_flag):
        start = time.time()
        run_date = date.today().strftime("%Y/%m/%d")
        total_row_count = df.height
        failed_records_write_location = 'N/A'
        failed_records_count = total_row_count - int(rule["value"])
        if total_row_count == int(rule["value"]):
            test_status = "PASS"
        else:
            test_status = "FAIL"
            failed_df = pl.DataFrame([], schema=df.schema).with_columns(
                [
                    pl.lit(run_date).alias("Run_Date"),
                    pl.lit("unique_keys").alias("Rule"),
                    pl.lit("All columns").alias("Column_Tested"),
                    pl.lit(1 if rule["ruletype"] == 'Mandatory' else 0).alias(
                        "Mandatory"),
                    pl.lit("NA").alias("job_id")
                ]
            )
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag, False)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)
    # ----- Function takes the filepath of ruleset as an input and apply validations defined in the ruleset.

    def read_csv_input_and_apply_validation(self, rules_csv_file_path, result_summery_file_path, file_path=None):
        input_df = pl.read_csv(rules_csv_file_path)
        rule_set = input_df.rows(named=True)
        new_tables = get_missing_tables(self.tables_list, rule_set)
        self.tables_list = {**self.tables_list, **new_tables}
        new_dataframes = read_dataset(
            new_tables, self.data_read_ob, self.no_of_partition, self.run_engine)
        if new_dataframes:
            self.dataframes = {**self.dataframes, **new_dataframes}
        self.df_rules_validation(rule_set, result_summery_file_path)

    def apply_validation(self, rule_config_df, write_summary_on_database=False, failed_schema_source_list=[], output_summary_folder_path='', write_failed_records_flag=True):
        try:
            rule_set = rule_config_df.rows(named=True)
        except:
            rule_set = rule_config_df.collect()
        new_tables = get_missing_tables(self.tables_list, rule_set)
        self.tables_list = {**self.tables_list, **new_tables}
        new_dataframes = read_dataset(
            new_tables, self.data_read_ob, self.no_of_partition, self.run_engine)
        if new_dataframes:
            self.dataframes = {**self.dataframes, **new_dataframes}
        self.df_rules_validation(rule_set, write_summary_on_database,
                                 failed_schema_source_list, output_summary_folder_path, write_failed_records_flag)

    # ----- Function include all the above functions and apply rule set at once and gives a consolidated result.

    def df_rules_validation(self, rule_set,  write_summary_on_database, failed_schema_source_list, result_summary_folder_path='', write_failed_records_flag=True):
        test_summary = []
        try:
            for rule in rule_set:
                try:
                    source = f'''{rule["source_type"]}_{rule["layer"]}_{rule["source_name"]}_{rule["filename"]}'''

                    if "failed_schema_source_list" in rule and rule['failed_schema_source_list'] in failed_schema_source_list:
                        run_date = date.today().strftime("%Y/%m/%d")
                        test_summary.append(data_quality_test_summary_tuple(
                            self.job_id, rule, "schema check fail", "", "", "", 0, run_date, modify_active=True))
                        continue

                    if 'active' in rule and int(rule['active']) == 0:
                        run_date = date.today().strftime("%Y/%m/%d")
                        test_summary.append(data_quality_test_summary_tuple(
                            self.job_id, rule, "", "", "", "", 0, run_date))
                        continue

                    if rule["rule_name"] == "null_check":
                        result_df = self.null_check(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)
                    elif rule["rule_name"] == "schema_check":
                        result_df = self.schema_check(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)
                    elif rule["rule_name"] == "range_min_check":
                        result_df = self.range_min_check(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)
                   # elif rule["rule_name"] == "range_min_inclusive_check":
                   #     result_df = self.range_min_inclusive_check(
                   #         self.dataframes[source], rule, write_failed_records_flag)
                   #     test_summary.append(result_df)
                    elif rule["rule_name"] == "range_max_check":
                        result_df = self.range_max_check(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)
                    elif rule["rule_name"] == "length_check":
                        result_df = self.length_check(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)
                    elif rule["rule_name"] == "unique_keys_check":
                        result_df = self.unique_keys_check(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)
                    elif rule["rule_name"] == "unique_records_check":
                        result_df = self.unique_records_check(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)
                    elif rule["rule_name"] == "allowed_values_check":
                        result_df = self.allowed_values_check(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)
                    elif rule["rule_name"] == "min_length_check":
                        result_df = self.min_length_check(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)
                    elif rule["rule_name"] == "column_count_check":
                        result_df = self.column_count_check(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)
                    elif rule["rule_name"] == "not_allowed_values_check":
                        result_df = self.not_allowed_values_check(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)
                    elif rule["rule_name"] == "date_range_check":
                        result_df = self.date_range_check(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)
                    elif rule["rule_name"] == "regex_check":
                        result_df = self.regex_check(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)
                    elif rule["rule_name"] == "row_count_check":
                        result_df = self.row_count_check(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)
                    else:
                        run_date = date.today().strftime("%Y/%m/%d")
                        test_summary.append(data_quality_test_summary_tuple(
                            self.job_id, rule, "invalid rule name", "", "", "", 0, run_date))
                        continue
                except Exception as e:
                    run_date = date.today().strftime("%Y/%m/%d")
                    test_summary.append(data_quality_test_summary_tuple(
                        self.job_id, rule, f"Exception :: {e}", "", "", "", 0, run_date))
                    continue

            summary_df = self.data_check_summarization(test_summary)
            if write_summary_on_database and self.data_right_structure == 'file':
                try:
                    DatabricksSqlDF().write_from_polars(
                        summary_df, self.output_db_name, 'diagnostic_summary')
                except:
                    raise Exception(
                        (f"Writing summary on hive database not supported."))
            if self.data_right_structure == 'file':
                if result_summary_folder_path.strip() != '':
                    summary_report_path = self.data_write_ob.write_from_polars(
                        summary_df, result_summary_folder_path, 'summary')
                    print(
                        f"Summary report is uploaded successfully at : {summary_report_path}")
                elif write_summary_on_database:
                    print(
                        f"Summary report is added successfully at : {self.output_db_name}.diagnostic_summary")
            else:
                summary_report_path = self.data_write_ob.write_from_polars(
                    summary_df, self.output_db_name, 'diagnostic_summary')
                print(
                    f"Summary report is added successfully at : {summary_report_path}")
        except Exception as e:
            raise Exception(e)
