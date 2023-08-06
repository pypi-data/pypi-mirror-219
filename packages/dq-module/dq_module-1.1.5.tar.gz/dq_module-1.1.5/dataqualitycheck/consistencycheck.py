from datetime import date, datetime
from .commonutilities import *
import polars as pl
try:
    import pyspark
    from pyspark.sql.functions import *
    from pyspark.sql.types import *
    from pyspark.context import SparkContext
    from pyspark.sql.session import SparkSession
except:
    pass


class ConsistencyCheck():
    def __init__(self, tables_list, interaction_between_tables, data_read_ob, data_write_ob, data_right_structure, job_id, time_zone=None, output_db_name="data_quality_output", no_of_partition=4, run_engine = 'pyspark'):
        self.data_read_ob = data_read_ob
        self.tables_list = tables_list
        self.interaction_between_tables = interaction_between_tables
        self.data_write_ob = data_write_ob
        self.data_right_structure = data_right_structure
        self.no_of_partition = no_of_partition
        self.run_engine = run_engine
        self.dataframes = read_dataset(self.tables_list, self.data_read_ob, self.no_of_partition, self.run_engine , True)
        self.output_db_name = output_db_name
        self.job_id = job_id
        self.consistency_check_summary = []
        self.time_zone = time_zone
        if self.run_engine.lower() == 'pyspark':
           self.spark = SparkSession(SparkContext.getOrCreate())
        else:
           pass


    def consistency_check(self, rule):
        base_table_source = f'''{rule["base_table_source_type"]}_{rule["base_table_layer"]}_{rule["base_table_source_name"]}_{rule["base_table_filename"]}'''
        base_table = self.dataframes[base_table_source]
        mapped_table_source = f'''{rule["mapped_table_source_type"]}_{rule["mapped_table_layer"]}_{rule["mapped_table_source_name"]}_{rule["mapped_table_filename"]}'''
        mapped_table = self.dataframes[mapped_table_source]
        base_table_col_name = rule["base_table_col_name"]
        mapped_table_col_name = rule["mapped_table_col_name"]
        rundate = date.today().strftime("%Y/%m/%d")
        base_table_source = f'''{rule["base_table_source_type"]}_{rule["base_table_layer"]}_{rule["base_table_source_name"]}_{rule["base_table_filename"]}'''
        mapped_table_source = f'''{rule["mapped_table_source_type"]}_{rule["mapped_table_layer"]}_{rule["mapped_table_source_name"]}_{rule["mapped_table_filename"]}'''
        base_table_sum = ''
        mapped_table_sum = ''
        difference_col = ''
        per_difference_col = ''
        desc = ''
        try:
            base_table_col_type = column_type_identifier(
                base_table, base_table_col_name, self.run_engine)
            mapped_table_col_type = column_type_identifier(
                mapped_table, mapped_table_col_name, self.run_engine)

            if base_table_col_type == mapped_table_col_type:
                if base_table_col_type == ColumnType.NUMERICAL.value:
                    if self.run_engine.lower() == 'polars':
                        base_table_sum = base_table.select(
                            pl.col(base_table_col_name).sum()).rows()[0][0]
                        mapped_table_sum = mapped_table.select(
                            pl.col(mapped_table_col_name).sum()).rows()[0][0]
                    else:
                        base_table_sum = base_table.select(
                            sum(base_table_col_name)).take(1)[0][0]
                        mapped_table_sum = mapped_table.select(
                            sum(mapped_table_col_name)).take(1)[0][0]
                else:
                    if self.run_engine.lower() == 'polars':
                        base_table=base_table.filter(pl.col(base_table_col_name).is_not_null())
                        base_table_sum = base_table.select(
                            pl.col(base_table_col_name).n_unique()).rows()[0][0]
                        mapped_table=mapped_table.filter(pl.col(mapped_table_col_name).is_not_null())
                        mapped_table_sum = mapped_table.select(
                            pl.col(mapped_table_col_name).n_unique()).rows()[0][0]
                    else:
                        base_table_sum = base_table.select(
                            countDistinct(base_table_col_name)).take(1)[0][0]
                        mapped_table_sum = mapped_table.select(
                            countDistinct(mapped_table_col_name)).take(1)[0][0]

                difference_col = base_table_sum - mapped_table_sum
                if difference_col == 0:
                    per_difference_col = 0.0
                else:
                    per_difference_col = (difference_col / base_table_sum)*100

                 # QUALITY DISCRIPTION COLUMN
                desc = str("Difference check between " + base_table_col_name + " and " +
                           mapped_table_col_name + " in tables " + base_table_source + " and " + mapped_table_source)

            else:
                desc = f"consistency check cannot be applicable for {base_table_col_name} and {mapped_table_col_name} columns"
        except Exception as e:
            desc = str(e)

        res = (self.job_id,
               rule["container_name"],
               rule["read_connector_method"],
               rule["base_table_source_type"],
               rule["base_table_layer"],
               rule["base_table_source_name"],
               rule["base_table_filename"],
               str(base_table_sum),
               rule["mapped_table_source_type"],
               rule["mapped_table_layer"],
               rule["mapped_table_source_name"],
               rule["mapped_table_filename"],
               str(mapped_table_sum),
               str(desc),
               str(difference_col),
               str(per_difference_col),
               rundate)
        self.consistency_check_summary.append(res)
        return res

    def table_info(self, tables_list, rule_set):
        new_tables = {}
        for rule in rule_set:
            base_table_source = f'''{rule["base_table_source_type"]}_{rule["base_table_layer"]}_{rule["base_table_source_name"]}_{rule["base_table_filename"]}'''
            mapped_table_source = f'''{rule["mapped_table_source_type"]}_{rule["mapped_table_layer"]}_{rule["mapped_table_source_name"]}_{rule["mapped_table_filename"]}'''
            if base_table_source not in tables_list.keys():
                new_tables[base_table_source] = {"read_connector_method": rule["read_connector_method"],
                                                 "container_name": rule["container_name"],
                                                 "latest_file_path": rule["base_table_file_path"],
                                                 "source_name": rule["base_table_source_name"],
                                                 "source_type": rule["base_table_source_type"],
                                                 "layer": rule["base_table_layer"],
                                                 "filename": rule["base_table_filename"]
                                                 }

            if mapped_table_source not in tables_list.keys():
                new_tables[mapped_table_source] = {"read_connector_method": rule["read_connector_method"],
                                                   "container_name": rule["container_name"],
                                                   "latest_file_path": rule["mapped_table_file_path"],
                                                   "source_name": rule["mapped_table_source_name"],
                                                   "source_type": rule["mapped_table_source_type"],
                                                   "layer": rule["mapped_table_layer"],
                                                   "filename": rule["mapped_table_filename"]
                                                   }
        return new_tables

    def summary_df_into_polars(self, test_summary):
        schema = get_schema(ConsistencyCheckSummaryStructure.COLUMN_NAME.value, ConsistencyCheckSummaryStructure.COLUMN_DATATYPE.value, self.run_engine.lower())
        df = pl.DataFrame(data=test_summary, columns=schema)
        return df

    def summary_df_into_spark(self, test_summary):
        schema = get_schema(ConsistencyCheckSummaryStructure.COLUMN_NAME.value, ConsistencyCheckSummaryStructure.COLUMN_DATATYPE.value, self.run_engine.lower())
        df = self.spark.createDataFrame(data=test_summary, schema=schema)
        return df

    def apply_consistency_check(self, rule_config_df ,output_report_folder_path=''):
        try:
          rule_set = rule_config_df.rows(named=True)
        except:
          rule_set = rule_config_df.collect()
        new_tables = self.table_info(self.tables_list, rule_set)
        self.tables_list = {**self.tables_list, **new_tables}
        new_dataframes = read_dataset(new_tables, self.data_read_ob, self.no_of_partition, self.run_engine , True)
        if new_dataframes:
            self.dataframes = {**self.dataframes, **new_dataframes}

        test_summary = []
        try:
            for rule in rule_set:
                result_df = self.consistency_check(rule)
                test_summary.append(result_df)

            if self.run_engine.lower() == 'polars':
                summary_df = self.summary_df_into_polars(test_summary)
            else:
                summary_df = self.summary_df_into_spark(test_summary)

            if self.data_right_structure == 'file':
            
                file_name = f"consistency_check_report{datetime.now(self.time_zone).strftime('_%d_%m_%Y_%H_%M_%S')}"
                if self.run_engine.lower() == 'polars':
                    report_file_path = self.data_write_ob.write_from_polars(summary_df, output_report_folder_path, file_name)
                else:
                    report_file_path = self.data_write_ob.write(summary_df, output_report_folder_path, file_name)
                print(f"Data consistency report is uploaded successfully at : {report_file_path}")
            else:
                if self.run_engine.lower() == 'polars':
                    report_file_path = self.data_write_ob.write_from_polars(summary_df, self.output_db_name, ModuleName.CONSISTENCYCHECK.value)
                else:
                    report_file_path = self.data_write_ob.write(summary_df, self.output_db_name, ModuleName.CONSISTENCYCHECK.value)
                print(f"Data consistency report is added successfully at : {report_file_path}")
        except Exception as e:
            raise Exception(e)
