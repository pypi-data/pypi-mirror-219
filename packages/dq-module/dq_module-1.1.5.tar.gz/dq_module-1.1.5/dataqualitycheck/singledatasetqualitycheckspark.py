from datetime import date,datetime
import time
from .commonutilities import *
from itertools import zip_longest
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


class SingleDatasetQualityCheckSpark():

    def __init__(self, tables_list, interaction_between_tables, data_read_ob, data_write_ob, data_right_structure, job_id, time_zone=None, output_db_name="data_quality_output", no_of_partition=4):
        self.spark = SparkSession(SparkContext.getOrCreate())
        self.data_read_ob = data_read_ob
        self.tables_list = tables_list
        self.interaction_between_tables = interaction_between_tables
        self.data_write_ob = data_write_ob
        self.data_right_structure = data_right_structure
        self.test_summary = []
        self.no_of_partition = no_of_partition
        self.run_engine = 'pyspark'
        self.dataframes = read_dataset(
            self.tables_list, self.data_read_ob, self.no_of_partition)
        self.output_db_name = output_db_name
        self.job_id = job_id
        self.time_zone = time_zone

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
                failed_records_write_location = self.data_write_ob.write(
                    failed_df, failed_record_folder_path, failed_record_file_name, rule)
            else:
                table_name = f'''{rule["source_type"]}_{rule["layer"]}_{rule["source_name"]}_{rule["filename"]}'''
                failed_records_write_location = self.data_write_ob.write(
                    failed_df, self.output_db_name, table_name)
        return failed_records_write_location

    def drift_report(self, config_col, dataframe_col):
        # indivisual data drift reports
        drift_df = self.spark.createDataFrame(zip_longest(config_col.split(','), dataframe_col), schema=['config_cols', 'dataframe_cols']).\
            withColumn('Drift', when((col('config_cols') == col('dataframe_cols')) & (col('config_cols').isNotNull()),
                                     "No Drift").otherwise('Drift'))
        return drift_df

    def date_format_function(self, infer_df, date_col_names, date_col_format, column_names, date_format_dictionary=None):
        try:
            self.spark.sql("set spark.sql.legacy.timeParserPolicy=CORRECTED")
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

                date_format_validate_udf = udf(lambda z: is_date_format_valid(z, date_format),BooleanType())
                failed_records = infer_df.withColumn(f"{date_column_name}_bad_record", date_format_validate_udf(date_column_name)).\
                    filter((col(f"{date_column_name}_bad_record") == False) | (col(f"{date_column_name}_bad_record").isNull())).drop(col(f"{date_column_name}_bad_record")).collect() 
                total_records_rows.extend(failed_records)

            total_records_df = self.spark.createDataFrame(total_records_rows, schema=eval(
                schema_enforce_structure(column_names, ",".join(['str']*len(column_names.split(','))))))
            total_records_df = total_records_df.dropDuplicates(total_records_df.columns)
        except Exception as e:
            raise Exception(e)
        return total_records_df
    
    def null_check_V1(self,df, rule, write_failed_records_flag):
        run_date = date.today().strftime("%Y/%m/%d")
        start = time.time()
        total_row_count = df.count()
        columnList = list(rule["column_to_be_checked"].split(","))

        result = self.spark.createDataFrame([], df.schema)
        column_passed = []
        column_failed = []
        for column in columnList:
            failed_results = df.filter(col(column).isNull())
            result = result.union(failed_results)
            result = result.dropDuplicates()
            failed_records_count = failed_results.count()
            failed_records_write_location = 'N/A'
            if failed_records_count == 0:
                column_passed.append(column)
            else:
                column_failed.append(column)
        
        total_failed_records_count = result.count()

        if len(column_passed) == len(columnList):
            test_status = "PASS"
        elif len(column_failed) == len(columnList):
            test_status = "FAIL"
        else:
            test_status = "Passed: {} and Failed: {}".format(", ".join(column_passed), ", ".join(column_failed))

        failed_df = result.withColumn("Run_Date", lit(run_date)).withColumn("Rule", lit(rule["rule_name"])).withColumn("Column_Tested", lit(rule["column_to_be_checked"])).withColumn("Mandatory", lit(1 if rule["ruletype"] == 'Mandatory' else 0).cast(LongType())).withColumn("job_id", lit(self.job_id))
     
        failed_records_write_location = self.write_failed_records(rule, failed_df, write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, total_failed_records_count, failed_records_write_location, start, run_date)

    # ----- Function to check if column have any null value.
    def null_check(self, df, rule, write_failed_records_flag):
        run_date = date.today().strftime("%Y/%m/%d")
        start = time.time()
        total_row_count = df.count()
        result = df.filter(col(rule["column_to_be_checked"]).isNull())
        failed_records_count = result.count()
        failed_records_write_location = 'N/A'
        if failed_records_count == 0:
            test_status = "PASS"
        else:
            test_status = "FAIL"
            failed_df = result.withColumn("Run_Date", lit(run_date)).withColumn("Rule", lit(rule["rule_name"])).withColumn("Column_Tested", lit(
                rule["column_to_be_checked"])).withColumn("Mandatory", lit(1 if rule["ruletype"] == 'Mandatory' else 0).cast(LongType())).withColumn("job_id", lit(self.job_id))
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

       # ----- Function to check if all the required columns exist.

    def schema_check(self, df, rule, write_failed_records_flag):
        run_date = date.today().strftime("%Y/%m/%d")
        start = time.time()
        date_col_config = eval(
            rule["date_column_config"]) if rule["date_column_config"] and rule["date_column_config"] != 'null' else {}
        total_row_count = df.count()
        failed_records_count = 0
        failed_records_write_location = 'N/A'
        reason = ''
        col_list = rule["column_to_be_checked"].split(',')
        value_list = rule["value"].split(',')
        try:
            # check if the config cols actually present or not
            if len(col_list) != len(value_list):
                raise Exception("missing column datatypes")
            if len(col_list) != len(df.columns):
                raise Exception("mismatch column count")

            config_cols_availability(
                df, rule["column_to_be_checked"], rule["layer"])

            if rule["column_to_be_checked"] != ",".join(df.columns):
                raise Exception("config column sequence mismatched")

            # getting the cols only in the col name column in config
            infer_df_config_cols = df.select(*rule["column_to_be_checked"].split(','))
            # date cols ka validation ke liye

            date_col_names = [col_list[data_index] for data_index in range(
                len(value_list)) if 'date' in str(value_list[data_index]).lower()]

            # check requirements to run the date check function or not
            failed_date_records_count = 0
            failed_date_records = self.spark.createDataFrame([], schema=eval(schema_enforce_structure(
                rule["column_to_be_checked"], rule["value"])))
            if len(date_col_names) > 0:
                failed_date_records = self.date_format_function(
                    infer_df_config_cols, date_col_names, date_col_config, rule["column_to_be_checked"], rule["date_format_dictionary"])
                failed_date_records_count = failed_date_records.count()

            # non date cols schema checkups
            non_date_cols = ','.join(
                [column for column in infer_df_config_cols.columns if column not in date_col_names])
            infer_df_selected_cols = infer_df_config_cols.select(
                *non_date_cols.split(','))  # non date cols only
            schema_enforce = eval(schema_enforce_structure(
                rule["column_to_be_checked"], rule["value"]))
            enforce_df_selected_cols = self.data_read_ob.read_enforce_schema_spark(rule, schema_enforce, self.no_of_partition)\
                .select(*non_date_cols.split(','))

            infer_df_selected_cols = infer_df_selected_cols.withColumn("concat_col", concat_ws("//", *infer_df_selected_cols.columns))
            enforce_df_selected_cols = enforce_df_selected_cols.withColumn("concat_col", concat_ws("//", *enforce_df_selected_cols.columns))
            failed_enforce_records = infer_df_selected_cols.join(enforce_df_selected_cols, on="concat_col", how='anti').drop("concat_col")  # failed records non date cols
            failed_enforce_records_count = failed_enforce_records.count()

            test_status = "PASS" if failed_enforce_records_count == 0 and failed_date_records_count == 0 else "FAIL"
            # if test_status == "PASS":
            #     if infer_df_selected_cols.schema != enforce_df_selected_cols.schema:
            #         raise Exception('schema is different.')
            # else:
            if test_status == "FAIL":

                # print(f"filename :: {rule['filename']} \n..............\n inferschema :: {infer_df_selected_cols.schema}")
                # infer_df_selected_cols.display()

                # print(f"enforceschema :: {enforce_df_selected_cols.schema}")
                # enforce_df_selected_cols.display()

                failed_records_count = failed_date_records_count + failed_enforce_records_count
                if failed_date_records_count != 0 and failed_enforce_records_count != 0:
                    failed_enforce_records_cols=failed_enforce_records.columns
                    #failed_enforce_records = failed_enforce_records.withColumn("concat_col", concat_ws("//", *failed_enforce_records.columns))
                    #failed_date_records = failed_date_records.withColumn("concat_col", concat_ws("//", *failed_enforce_records_cols))
                    failed_df = failed_enforce_records.join(failed_date_records, on=failed_enforce_records_cols, how='outer')
                    reason = ', wrong data type and date format'
                elif failed_date_records_count != 0:
                    failed_df = failed_date_records
                    reason = ', wrong date format'
                else:
                    failed_df = failed_enforce_records
                    reason = ', wrong data type'

                failed_df = failed_df.withColumn("Run_Date", lit(run_date)).withColumn("Rule", lit(rule["rule_name"]))\
                    .withColumn("Column_Tested", lit("All columns")).withColumn("Mandatory", lit(1 if rule["ruletype"] == 'Mandatory' else 0).cast(LongType())).withColumn("job_id", lit(self.job_id))
                failed_records_write_location = self.write_failed_records(
                    rule, failed_df, write_failed_records_flag, False)

        except Exception as e:
            test_status = "FAIL"
            failed_records_count = total_row_count
            reason = f', {e}'
            failed_df = df.withColumn("Run_Date", lit(run_date)).withColumn("Rule", lit(rule["rule_name"]))\
                .withColumn("Column_Tested", lit("All columns")).withColumn("Mandatory", lit(1 if rule["ruletype"] == 'Mandatory' else 0).cast(LongType())).withColumn("job_id", lit(self.job_id))
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag, False)
        return data_quality_test_summary_tuple(self.job_id, rule, test_status + reason, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

    def range_min_check_V1(self, df, rule, write_failed_records_flag):
        run_date = date.today().strftime("%Y/%m/%d")
        start = time.time()
        total_row_count = df.count()
        columnList = list(rule["column_to_be_checked"].split(","))
        valueList = list(rule["value"].split(','))

        if len(columnList)==len(valueList):
            combined_list = zip(columnList,valueList)
        else:
            raise Exception("missing values/columns")

        result = self.spark.createDataFrame([], df.schema)
        column_passed = []
        column_failed = []
        for column_value_tuple in combined_list:
            df = df.filter(col(column_value_tuple[0]).isNotNull())
            failed_results = df.filter(col(column_value_tuple[0]) < float(column_value_tuple[1]))
            result = result.union(failed_results)
            result = result.dropDuplicates()
            failed_records_count = failed_results.count()
            failed_records_write_location = 'N/A'
            if failed_records_count == 0:
                column_passed.append(column_value_tuple[0])
            else:
                column_failed.append(column_value_tuple[0])
        
        total_failed_records_count = result.count()

        if len(column_passed) == len(columnList):
            test_status = "PASS"
        elif len(column_failed) == len(columnList):
            test_status = "FAIL"
        else:
            test_status = "Passed: {} and Failed: {}".format(", ".join(column_passed), ", ".join(column_failed))

        failed_df = result.withColumn("Run_Date", lit(run_date)).withColumn("Rule", lit(rule["rule_name"])).withColumn("Column_Tested", lit(rule["column_to_be_checked"])).withColumn("Mandatory", lit(1 if rule["ruletype"] == 'Mandatory' else 0).cast(LongType())).withColumn("job_id", lit(self.job_id))
    
        failed_records_write_location = self.write_failed_records(rule, failed_df, write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, total_failed_records_count, failed_records_write_location, start, run_date)

    # ----- Function to check if values not be less than the given value

    def range_min_check(self, df, rule, write_failed_records_flag):
        run_date = date.today().strftime("%Y/%m/%d")
        start = time.time()
        total_row_count = df.count()
        df = df.filter(col(rule["column_to_be_checked"]).isNotNull())
        result = df.filter(
            col(rule["column_to_be_checked"]) < float(rule["value"]))
        failed_records_count = result.count()
        failed_records_write_location = 'N/A'
        if failed_records_count == 0:
            test_status = "PASS"
        else:
            test_status = "FAIL"
            failed_df = result.withColumn("Run_Date", lit(run_date)).withColumn("Rule", lit(rule["rule_name"]))\
                .withColumn("Column_Tested", lit(f"{rule['column_to_be_checked']}:{rule['value']}")).withColumn("Mandatory", lit(1 if rule["ruletype"] == 'Mandatory' else 0).cast(LongType())).withColumn("job_id", lit(self.job_id))
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

  #  # ----- Function to check if values should not be less than or equal to the required value
  #  def range_min_inclusive_check(self, df, rule, write_failed_records_flag):
  #     run_date = date.today().strftime("%Y/%m/%d")
  #      start = time.time()
  #     total_row_count = df.count()
  #     df = df.filter(col(rule["column_to_be_checked"]).isNotNull())
  #     result = df.filter(
  #          col(rule["column_to_be_checked"]) <= float(rule["value"]))
  #      failed_records_count = result.count()
  #      failed_records_write_location = 'N/A'
  #     if failed_records_count == 0:
  #         test_status = "PASS"
  #     else:
  #          test_status = "FAIL"
  #          failed_df = result.withColumn("Run_Date", lit(run_date)).withColumn("Rule", lit(rule["rule_name"]))\
  #             .withColumn("Column_Tested", lit(f"{rule['column_to_be_checked']}:{rule['value']}")).withColumn("Mandatory", lit(1 if rule["ruletype"] == 'Mandatory' else 0).cast(LongType())).withColumn("job_id", lit(self.job_id))
  #         failed_records_write_location = self.write_failed_records(
  #             rule, failed_df, write_failed_records_flag)
  #
  #      return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)
    def range_max_check_V1(self, df, rule, write_failed_records_flag):
        run_date = date.today().strftime("%Y/%m/%d")
        start = time.time()
        total_row_count = df.count()
        columnList = list(rule["column_to_be_checked"].split(","))
        valueList = list(rule["value"].split(','))

        if len(columnList)==len(valueList):
            combined_list = zip(columnList,valueList)
        else:
            raise Exception("missing values/columns")

        result = self.spark.createDataFrame([], df.schema)
        column_passed = []
        column_failed = []
        for column_value_tuple in combined_list:
            df = df.filter(col(column_value_tuple[0]).isNotNull())
            failed_results = df.filter(col(column_value_tuple[0]) > float(column_value_tuple[1]))
            result = result.union(failed_results)
            result = result.dropDuplicates()
            failed_records_count = failed_results.count()
            failed_records_write_location = 'N/A'
            if failed_records_count == 0:
                column_passed.append(column_value_tuple[0])
            else:
                column_failed.append(column_value_tuple[0])
        
        total_failed_records_count = result.count()

        if len(column_passed) == len(columnList):
            test_status = "PASS"
        elif len(column_failed) == len(columnList):
            test_status = "FAIL"
        else:
            test_status = "Passed: {} and Failed: {}".format(", ".join(column_passed), ", ".join(column_failed))

        failed_df = result.withColumn("Run_Date", lit(run_date)).withColumn("Rule", lit(rule["rule_name"])).withColumn("Column_Tested", lit(rule["column_to_be_checked"])).withColumn("Mandatory", lit(1 if rule["ruletype"] == 'Mandatory' else 0).cast(LongType())).withColumn("job_id", lit(self.job_id))
    
        failed_records_write_location = self.write_failed_records(rule, failed_df, write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, total_failed_records_count, failed_records_write_location, start, run_date)
    # ----- Function to check if values should not be greater then the given value
    def range_max_check(self, df, rule, write_failed_records_flag):
        run_date = date.today().strftime("%Y/%m/%d")
        start = time.time()
        total_row_count = df.count()
        df = df.filter(col(rule["column_to_be_checked"]).isNotNull())
        result = df.filter(
            col(rule["column_to_be_checked"]) > float(rule["value"]))
        failed_records_count = result.count()
        failed_records_write_location = 'N/A'
        if failed_records_count == 0:
            test_status = "PASS"
        else:
            test_status = "FAIL"
            failed_df = result.withColumn("Run_Date", lit(run_date)).withColumn("Rule", lit(rule["rule_name"]))\
                .withColumn("Column_Tested", lit(f"{rule['column_to_be_checked']}:{rule['value']}")).withColumn("Mandatory", lit(1 if rule["ruletype"] == 'Mandatory' else 0).cast(LongType())).withColumn("job_id", lit(self.job_id))
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)
    
    def length_check_V1(self, df, rule, write_failed_records_flag):
        run_date = date.today().strftime("%Y/%m/%d")
        start = time.time()
        total_row_count = df.count()
        columnList = list(rule["column_to_be_checked"].split(","))
        valueList = list(rule["value"].split(','))

        if len(columnList)==len(valueList):
            combined_list = zip(columnList,valueList)
        else:
            raise Exception("missing values/columns")

        result = self.spark.createDataFrame([], df.schema)
        column_passed = []
        column_failed = []
        for column_value_tuple in combined_list:
            failed_results = df.filter(
            length(col(column_value_tuple[0])) > int(column_value_tuple[1]))
            result = result.union(failed_results)
            result = result.dropDuplicates()
            failed_records_count = failed_results.count()
            failed_records_write_location = 'N/A'
            if failed_records_count == 0:
                column_passed.append(column_value_tuple[0])
            else:
                column_failed.append(column_value_tuple[0])
        
        total_failed_records_count = result.count()

        if len(column_passed) == len(columnList):
            test_status = "PASS"
        elif len(column_failed) == len(columnList):
            test_status = "FAIL"
        else:
            test_status = "Passed: {} and Failed: {}".format(", ".join(column_passed), ", ".join(column_failed))

        failed_df = result.withColumn("Run_Date", lit(run_date)).withColumn("Rule", lit(rule["rule_name"])).withColumn("Column_Tested", lit(rule["column_to_be_checked"])).withColumn("Mandatory", lit(1 if rule["ruletype"] == 'Mandatory' else 0).cast(LongType())).withColumn("job_id", lit(self.job_id))
    
        failed_records_write_location = self.write_failed_records(rule, failed_df, write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, total_failed_records_count, failed_records_write_location, start, run_date)
    
    
    # ----- Function to check if the values in the column have given length or not.
    def length_check(self, df, rule, write_failed_records_flag):
        run_date = date.today().strftime("%Y/%m/%d")
        start = time.time()
        total_row_count = df.count()
        result = df.filter(
            length(col(rule["column_to_be_checked"])) > int(rule["value"]))
        failed_records_count = result.count()
        failed_records_write_location = 'N/A'
        if failed_records_count == 0:
            test_status = "PASS"
        else:
            test_status = "FAIL"
            failed_df = result.withColumn("Run_Date", lit(run_date)).withColumn("Rule", lit(rule["rule_name"]))\
                .withColumn("Column_Tested", lit(f"{rule['column_to_be_checked']}:{rule['value']}")).withColumn("Mandatory", lit(1 if rule["ruletype"] == 'Mandatory' else 0).cast(LongType())).withColumn("job_id", lit(self.job_id))
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

    # ----- Function to check if all the records are unique or not in the table.
    def unique_records_check(self, df, rule, write_failed_records_flag):
        run_date = date.today().strftime("%Y/%m/%d")
        start = time.time()
        total_row_count = df.count()
        columnList = df.columns
        d = df.groupBy(columnList).count().filter(
            col("count") == 1).drop("count")
        result = df.exceptAll(d)
        failed_records_count = result.count()
        failed_records_write_location = 'N/A'
        if failed_records_count == 0:
            test_status = "PASS"
        else:
            test_status = "FAIL"
            failed_df = result.withColumn("Run_Date", lit(run_date)).withColumn("Rule", lit(rule["rule_name"]))\
                .withColumn("Column_Tested", lit("All columns")).withColumn("Mandatory", lit(1 if rule["ruletype"] == 'Mandatory' else 0).cast(LongType())).withColumn("job_id", lit(self.job_id))
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag, False)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date, False, ",".join(df.columns))

    # ----- Function to check if all the records are unique for all given input columns.It takes a list of columns as an arguement
    def unique_keys_check(self, df, rule, write_failed_records_flag):
        run_date = date.today().strftime("%Y/%m/%d")
        start = time.time()
        total_row_count = df.count()
        columnList = list(rule["column_to_be_checked"].split(","))
        d = df.groupBy(columnList).count().filter(col("count") > 1).drop("count")
        d= d.withColumn("concat_col", concat_ws("//", *columnList))
        df1 = df.withColumn("concat_col", concat_ws("//", *columnList))
        result = df1.join(d, on="concat_col", how='leftsemi').select(df.columns)
        failed_records_count = result.count()
        failed_records_write_location = 'N/A'
        if failed_records_count == 0:
            test_status = "PASS"
        else:
            test_status = "FAIL"
            failed_df = result.withColumn("Run_Date", lit(run_date)).withColumn("Rule", lit(rule["rule_name"]))\
                .withColumn("Column_Tested", lit(f"{rule['column_to_be_checked']}:{rule['value']}")).withColumn("Mandatory", lit(1 if rule["ruletype"] == 'Mandatory' else 0).cast(LongType())).withColumn("job_id", lit(self.job_id))
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

    # ----- Function takes a list of allowed values for a particular column and check if the values of the column belongs to that list or not.
    def allowed_values_check(self, df, rule, write_failed_records_flag):
        run_date = date.today().strftime("%Y/%m/%d")
        start = time.time()
        total_row_count = df.count()
        result = df.filter(~col(rule["column_to_be_checked"]).isin(
            rule["value"].strip().split(',')) | col(rule["column_to_be_checked"]).isNull())
        failed_records_count = result.count()
        failed_records_write_location = 'N/A'
        if failed_records_count == 0:
            test_status = "PASS"
        else:
            test_status = "FAIL"
            failed_df = result.withColumn("Run_Date", lit(run_date)).withColumn("Rule", lit(rule["rule_name"]))\
                .withColumn("Column_Tested", lit(f"{rule['column_to_be_checked']}:{rule['value']}")).withColumn("Mandatory", lit(1 if rule["ruletype"] == 'Mandatory' else 0).cast(LongType())).withColumn("job_id", lit(self.job_id))
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)
    
    def min_length_check_V1(self, df, rule, write_failed_records_flag):
        run_date = date.today().strftime("%Y/%m/%d")
        start = time.time()
        total_row_count = df.count()
        columnList = list(rule["column_to_be_checked"].split(","))
        valueList = list(rule["value"].split(','))

        if len(columnList)==len(valueList):
            combined_list = zip(columnList,valueList)
        else:
            raise Exception("missing values/columns")

        result = self.spark.createDataFrame([], df.schema)
        column_passed = []
        column_failed = []
        for column_value_tuple in combined_list:
            failed_results = df.filter(
            length(col(column_value_tuple[0])) < int(column_value_tuple[1]))
            result = result.union(failed_results)
            result = result.dropDuplicates()
            failed_records_count = failed_results.count()
            failed_records_write_location = 'N/A'
            if failed_records_count == 0:
                column_passed.append(column_value_tuple[0])
            else:
                column_failed.append(column_value_tuple[0])
        
        total_failed_records_count = result.count()

        if len(column_passed) == len(columnList):
            test_status = "PASS"
        elif len(column_failed) == len(columnList):
            test_status = "FAIL"
        else:
            test_status = "Passed: {} and Failed: {}".format(", ".join(column_passed), ", ".join(column_failed))

        failed_df = result.withColumn("Run_Date", lit(run_date)).withColumn("Rule", lit(rule["rule_name"])).withColumn("Column_Tested", lit(rule["column_to_be_checked"])).withColumn("Mandatory", lit(1 if rule["ruletype"] == 'Mandatory' else 0).cast(LongType())).withColumn("job_id", lit(self.job_id))
    
        failed_records_write_location = self.write_failed_records(rule, failed_df, write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, total_failed_records_count, failed_records_write_location, start, run_date)
    
    # ----- Function to check that if the values in the column has the required minimum length or not.
    def min_length_check(self, df, rule, write_failed_records_flag):
        run_date = date.today().strftime("%Y/%m/%d")
        start = time.time()
        total_row_count = df.count()
        result = df.filter(
            length(col(rule["column_to_be_checked"])) < int(rule["value"]))
        failed_records_count = result.count()
        failed_records_write_location = 'N/A'
        if failed_records_count == 0:
            test_status = "PASS"
        else:
            test_status = "FAIL"
            failed_df = result.withColumn("Run_Date", lit(run_date)).withColumn("Rule", lit(rule["rule_name"]))\
                .withColumn("Column_Tested", lit(f"{rule['column_to_be_checked']}:{rule['value']}")).withColumn("Mandatory", lit(1 if rule["ruletype"] == 'Mandatory' else 0).cast(LongType())).withColumn("job_id", lit(self.job_id))
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

    # ----- Function to check that the table has required column count or not.
    def column_count_check(self, df, rule, write_failed_records_flag):
        run_date = date.today().strftime("%Y/%m/%d")
        start = time.time()
        total_row_count = df.count()
        total_col_count = len(df.columns)
        failed_records_count = total_col_count - int(rule["value"])
        failed_records_write_location = 'N/A'
        if total_col_count == int(rule["value"]):
            test_status = "PASS"
        else:
            test_status = "FAIL"
            result = self.spark.createDataFrame(
                data=[tuple([None for x in df.columns])], schema=df.schema)
            failed_df = result.withColumn("Run_Date", lit(run_date)).withColumn("Rule", lit(f"{rule['rule_name']}:{rule['value']}"))\
                .withColumn("Column_Tested", lit(f"All_Columns:{total_col_count}")).withColumn("Mandatory", lit(1 if rule["ruletype"] == 'Mandatory' else 0).cast(LongType())).withColumn("job_id", lit(self.job_id))
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag, False)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

    # ----- Function takes a list of not allowed values for a particular column and check if the column has not allowed values or not.
    def not_allowed_values_check(self, df, rule, write_failed_records_flag):
        run_date = date.today().strftime("%Y/%m/%d")
        start = time.time()
        total_row_count = df.count()
        result = df.filter(
            col(rule["column_to_be_checked"]).isin(rule["value"].strip().split(',')))
        failed_records_count = result.count()
        failed_records_write_location = 'N/A'
        if failed_records_count == 0:
            test_status = "PASS"
        else:
            test_status = "FAIL"
            failed_df = result.withColumn("Run_Date", lit(run_date)).withColumn("Rule", lit(rule["rule_name"]))\
                .withColumn("Column_Tested", lit(f"{rule['column_to_be_checked']}:{rule['value']}")).withColumn("Mandatory", lit(1 if rule["ruletype"] == 'Mandatory' else 0).cast(LongType())).withColumn("job_id", lit(self.job_id))
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

    # ----- Function to check if the date lies in the given range or not.
    def date_range_check(self, df, rule, write_failed_records_flag):
        run_date = date.today().strftime("%Y/%m/%d")
        start = time.time()
        total_row_count = df.count()
        value = eval(rule["value"]) 
        date_column_config = eval(rule["date_column_config"])
        
        min_value= parse( value["min_value"] )
        max_value= parse( value["max_value"] )
        
        if df.schema[rule["column_to_be_checked"]].dataType == StringType() :
          df1= df.withColumn("new_date",to_date(col(rule["column_to_be_checked"]) , date_column_config[rule["column_to_be_checked"]]))
          if df1.filter(col("new_date").isNull()).count() != df1.filter(col(rule["column_to_be_checked"]).isNull()).count():
             raise Exception("Wrong date format in date column config")
          else:
             result = df1.filter(~col("new_date").between(min_value,max_value)).drop("new_date")
        else:
           if datetime.strftime(df.first()[rule["column_to_be_checked"]], "%Y-%m-%d")==str(df.first()[rule["column_to_be_checked"]]):
               result = df.filter(~col(rule["column_to_be_checked"]).between(min_value,max_value))
           else:
              df1 = df.withColumn("new_date",to_date(col(rule["column_to_be_checked"]) , date_column_config[rule["column_to_be_checked"]]))
              result = df1.filter(~col("new_date").between(min_value,max_value)).drop("new_date")
           
          
        failed_records_count = result.count()
        failed_records_write_location = 'N/A'
        if failed_records_count == 0:
            test_status = "PASS"
        else:
            test_status = "FAIL"
            failed_df = result.withColumn("Run_Date", lit(run_date)).withColumn("Rule", lit(rule["rule_name"]))\
                .withColumn("Column_Tested", lit(f"{rule['column_to_be_checked']}:{value['min_value']},{value['max_value']}")).withColumn("Mandatory", lit(1 if rule["ruletype"] == 'Mandatory' else 0).cast(LongType())).withColumn("job_id", lit(self.job_id))
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

    # ----- Function to check if the given column matches the given regex pattern or not.
    def regex_check(self, df, rule, write_failed_records_flag):
        run_date = date.today().strftime("%Y/%m/%d")
        start = time.time()
        total_row_count = df.count()
        result = df.filter(
            ~col(rule["column_to_be_checked"]).rlike(rule["value"]))
        failed_records_count = result.count()
        failed_records_write_location = 'N/A'
        test_status = "PASS" if failed_records_count == 0 else "FAIL"

        if failed_records_count > 0:
            failed_df = result.withColumn("Run_Date", lit(run_date)).withColumn("Rule", lit(rule["rule_name"])).withColumn("Column_Tested", lit(
                f"{rule['column_to_be_checked']}:{rule['value']}")).withColumn("Mandatory", lit(1 if rule["ruletype"] == 'Mandatory' else 0).cast(LongType())).withColumn("job_id", lit(self.job_id))
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

    def row_count_check(self, df, rule, write_failed_records_flag):
        run_date = date.today().strftime("%Y/%m/%d")
        start = time.time()
        total_row_count = df.count()
        failed_records_write_location = 'N/A'
        failed_records_count = total_row_count - int(rule["value"])
        if total_row_count == int(rule["value"]):
            test_status = "PASS"
        else:
            test_status = "FAIL"
            failed_df = self.spark.createDataFrame([], schema=df.schema).withColumn("Run_Date", lit(run_date)).withColumn("Rule", lit(rule["rule_name"]))\
                .withColumn("Column_Tested", lit("All columns")).withColumn("Mandatory", lit(1 if rule["ruletype"] == 'Mandatory' else 0).cast(LongType())).withColumn("job_id", lit(self.job_id))
            failed_records_write_location = self.write_failed_records(
                rule, failed_df, write_failed_records_flag, False)

        return data_quality_test_summary_tuple(self.job_id, rule, test_status, total_row_count, failed_records_count, failed_records_write_location, start, run_date)

# ----- Function takes the filepath of ruleset as an input and apply validations defined in the ruleset.
    def read_csv_input_and_apply_validation(self, rules_csv_file_path, result_summery_file_path, file_path=None):
        input_df = self.spark.read.option(
            "header", True).csv(rules_csv_file_path)
        rule_set = input_df.collect()
        new_tables = get_missing_tables(self.tables_list, rule_set)
        self.tables_list = {**self.tables_list, **new_tables}
        new_dataframes = read_dataset(
            new_tables, self.data_read_ob, self.no_of_partition)
        if new_dataframes:
            self.dataframes = {**self.dataframes, **new_dataframes}
        self.df_rules_validation(rule_set, result_summery_file_path)

    def apply_validation(self, rule_config_df, write_summary_on_database=True, failed_schema_source_list=[], output_summary_folder_path='', write_failed_records_flag=True):
        rule_set = rule_config_df.collect()
        new_tables = get_missing_tables(self.tables_list, rule_set)
        self.tables_list = {**self.tables_list, **new_tables}
        new_dataframes = read_dataset(
            new_tables, self.data_read_ob, self.no_of_partition)
        if new_dataframes:
            self.dataframes = {**self.dataframes, **new_dataframes}
        self.df_rules_validation(rule_set, write_summary_on_database,
                                 failed_schema_source_list, output_summary_folder_path, write_failed_records_flag)

    # ----- Function include all the above functions and apply rule set at once and gives a consolidated result.

    def df_rules_validation(self, rule_set, write_summary_on_database, failed_schema_source_list, result_summary_folder_path, write_failed_records_flag):
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

                    if rule["rule_name"] == "null_check" and len(list(rule["column_to_be_checked"].split(",")))==1:
                        result_df = self.null_check(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)

                    elif rule["rule_name"] == "null_check" and len(list(rule["column_to_be_checked"].split(",")))>1:
                        result_df = self.null_check_V1(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)
                    
                    elif rule["rule_name"] == "schema_check":
                        result_df = self.schema_check(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)

                    elif rule["rule_name"] == "range_min_check" and len(list(rule["column_to_be_checked"].split(",")))==1:
                        result_df = self.range_min_check(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)

                    elif rule["rule_name"] == "range_min_check" and len(list(rule["column_to_be_checked"].split(",")))>1:
                        result_df = self.range_min_check_V1(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)
                    #elif rule["rule_name"] == "range_min_inclusive_check":
                    #    result_df = self.range_min_inclusive_check(
                    #       self.dataframes[source], rule, write_failed_records_flag)
                    #    test_summary.append(result_df)
                    elif rule["rule_name"] == "range_max_check" and len(list(rule["column_to_be_checked"].split(",")))==1:
                        result_df = self.range_max_check(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)
                    
                    elif rule["rule_name"] == "range_max_check" and len(list(rule["column_to_be_checked"].split(",")))>1:
                        result_df = self.range_max_check_V1(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)
                    
                    elif rule["rule_name"] == "length_check" and len(list(rule["column_to_be_checked"].split(",")))==1:
                        result_df = self.length_check(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)

                    elif rule["rule_name"] == "length_check" and len(list(rule["column_to_be_checked"].split(",")))>1:
                        result_df = self.length_check_V1(
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
                    elif rule["rule_name"] == "min_length_check" and len(list(rule["column_to_be_checked"].split(",")))==1 :
                        result_df = self.min_length_check(
                            self.dataframes[source], rule, write_failed_records_flag)
                        test_summary.append(result_df)
                    
                    elif rule["rule_name"] == "min_length_check" and len(list(rule["column_to_be_checked"].split(",")))>1 :
                        result_df = self.min_length_check_V1(
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

            summary_df = data_check_summarization_spark_df(
                self.spark, test_summary)
            if write_summary_on_database and self.data_right_structure == 'file':
                DatabricksSqlDF().write(summary_df, self.output_db_name, 'diagnostic_summary')
                summary_df = self.spark.sql(
                    f"select * from {self.output_db_name}.diagnostic_summary").filter(col('job_id') == self.job_id)
            if self.data_right_structure == 'file':
                if result_summary_folder_path.strip() != '':
                    summary_report_path = self.data_write_ob.write(
                        summary_df, result_summary_folder_path, 'summary')
                    print(
                        f"Summary report is uploaded successfully at : {summary_report_path}")
                elif write_summary_on_database:
                    print(
                        f"Summary report is added successfully at : {self.output_db_name}.diagnostic_summary")
            else:
                summary_report_path = self.data_write_ob.write(
                    summary_df, self.output_db_name, 'diagnostic_summary')
                print(
                    f"Summary report is added successfully at : {summary_report_path}")
        except Exception as e:
            raise Exception(e)
