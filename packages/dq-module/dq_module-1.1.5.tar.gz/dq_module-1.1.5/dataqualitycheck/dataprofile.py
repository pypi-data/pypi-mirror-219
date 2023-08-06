from datetime import date, datetime
import operator
import itertools
from .commonutilities import *
try:
    import pyspark
    from pyspark.sql.functions import *
    from pyspark.sql.types import *
    from pyspark.context import SparkContext
    from pyspark.sql.session import SparkSession
except:
    pass

class DataProfile():
    def __init__(self, tables_list, interaction_between_tables, data_read_ob, data_write_ob, data_right_structure, job_id, time_zone=None, no_of_partition=4, output_db_name="data_quality_output", run_engine='pyspark'):

        self.tables_list = tables_list
        self.interaction_between_tables = interaction_between_tables
        self.data_write_ob = data_write_ob
        self.data_read_ob = data_read_ob
        self.data_right_structure = data_right_structure
        self.no_of_partition = no_of_partition
        self.run_engine = run_engine
        self.dataframes = read_dataset(
            self.tables_list, self.data_read_ob, self.no_of_partition, self.run_engine, True)
        self.output_db_name = output_db_name
        self.job_id = job_id
        self.time_zone = time_zone
        if self.run_engine.lower() == 'polars':
            self.data_profiling_schema = get_schema(DataProfileReportStructure.COLUMN_NAME.value, DataProfileReportStructure.COLUMN_DATATYPE.value, 'polars')
        else:
            self.spark = SparkSession(SparkContext.getOrCreate())
            self.data_profiling_schema = get_schema(DataProfileReportStructure.COLUMN_NAME.value, DataProfileReportStructure.COLUMN_DATATYPE.value, 'pyspark')

    def apply_data_profiling_to_column_spark(self, df, source_type, layer, source_name, filename, column_to_be_checked, rows, columns):
        column_type = column_type_identifier(
            df, column_to_be_checked, self.run_engine)
        list_of_uniq = self.list_of_uniques_spark(df, column_to_be_checked)
        rundate = date.today().strftime("%Y/%m/%d")
        if column_type == ColumnType.NUMERICAL.value:
            result_data = df.agg(lit(self.job_id),
                                 lit(source_type),
                                 lit(layer),
                                 lit(source_name),
                                 lit(filename),
                                 lit(column_to_be_checked).alias(
                                     "column_name"),
                                 lit(column_type).alias("column_type"),
                                 lit(columns),
                                 lit(rows),
                                 min(column_to_be_checked).alias("min"),
                                 max(column_to_be_checked).alias("max"),
                                 avg(column_to_be_checked).alias("avg"),
                                 sum(column_to_be_checked).alias("sum"),
                                 stddev(column_to_be_checked).alias("stddev"),
                                 percentile_approx(
                                     column_to_be_checked, 0.25).alias("25th_per"),
                                 percentile_approx(
                                     column_to_be_checked, 0.50).alias("50th_per"),
                                 percentile_approx(
                                     column_to_be_checked, 0.75).alias("75th_per"),
                                 sum(when(col(column_to_be_checked).isNull(), 1).otherwise(
                                     0)).alias("missing_count"),
                                 countDistinct(column_to_be_checked).alias(
                                     "unique_count"),
                                 lit(None).alias("mode"),
                                 lit(list_of_uniq).alias("list_of_uniques"),
                                 lit(rundate).alias("run_date"))

        elif column_type == ColumnType.CATEGORICAL.value:
            mode = self.find_mode_spark(df, column_to_be_checked)
            result_data = df.agg(lit(self.job_id),
                                 lit(source_type),
                                 lit(layer),
                                 lit(source_name),
                                 lit(filename),
                                 lit(column_to_be_checked).alias(
                                     "column_name"),
                                 lit(column_type).alias("column_type"),
                                 lit(columns),
                                 lit(rows),
                                 lit(None),
                                 lit(None),
                                 lit(None),
                                 lit(None),
                                 lit(None),
                                 lit(None),
                                 lit(None),
                                 lit(None),
                                 sum(when(col(column_to_be_checked).isNull(), 1).otherwise(
                                     0)).alias("missing_count"),
                                 countDistinct(column_to_be_checked).alias(
                                     "unique_count"),
                                 lit(mode).alias("mode"),
                                 lit(list_of_uniq).alias("list_of_uniques"),
                                 lit(rundate).alias("run_date")
                                 )

        else:
            mode = self.find_mode_spark(df, column_to_be_checked)
            result_data = df.agg(lit(self.job_id),
                                 lit(source_type),
                                 lit(layer),
                                 lit(source_name),
                                 lit(filename),
                                 lit(column_to_be_checked).alias(
                                     "column_name"),
                                 lit(column_type).alias("column_type"),
                                 lit(columns),
                                 lit(rows),
                                 min(column_to_be_checked).alias("min"),
                                 max(column_to_be_checked).alias("max"),
                                 lit(None),
                                 lit(None),
                                 lit(None),
                                 percentile_approx(column_to_be_checked,
                                                   0.25).alias("25th_per"),
                                 percentile_approx(column_to_be_checked,
                                                   0.50).alias("50th_per"),
                                 percentile_approx(column_to_be_checked,
                                                   0.75).alias("75th_per"),
                                 sum(when(col(column_to_be_checked).isNull(),
                                          1).otherwise(0)).alias("missing_count"),
                                 countDistinct(column_to_be_checked).alias(
                                     "unique_count"),
                                 lit(mode).alias("mode"),
                                 lit(list_of_uniq).alias("list_of_uniques"),
                                 lit(rundate).alias("run_date")
                                 )
        return result_data

    def apply_data_profiling_to_column_polars(self, df, source_type, layer, source_name, filename, column_to_be_checked, rows, columns):
        column_type = column_type_identifier(
            df, column_to_be_checked, self.run_engine)
        list_of_uniq = self.list_of_uniques_polars(df, column_to_be_checked)
        rundate = date.today().strftime("%Y/%m/%d")
        if column_type == ColumnType.NUMERICAL.value:
            result_data = df.select([pl.lit(self.job_id).alias("job_id"),
                                     pl.lit(source_type).alias("source_type"),
                                     pl.lit(layer).alias("layer"),
                                     pl.lit(source_name).alias("source_name"),
                                     pl.lit(filename).alias("filename"),
                                     pl.lit(column_to_be_checked).alias(
                                         "column_name"),
                                     pl.lit(column_type).alias("column_type"),
                                     pl.lit(columns).alias(
                                         "total_column_count"),
                                     pl.lit(rows).alias("total_row_count"),
                                     pl.col(column_to_be_checked).min().alias(
                                         "min"),
                                     pl.col(column_to_be_checked).max().alias(
                                         "max"),
                                     pl.col(column_to_be_checked).mean().alias(
                                         "avg"),
                                     pl.col(column_to_be_checked).sum().alias(
                                         "sum"),
                                     pl.col(column_to_be_checked).std().alias(
                                         "stddev"),
                                     pl.col(column_to_be_checked).quantile(
                                         0.25).alias("25th_per"),
                                     pl.col(column_to_be_checked).quantile(
                                         0.50).alias("50th_per"),
                                     pl.col(column_to_be_checked).quantile(
                                         0.75).alias("75th_per"),
                                     pl.col(column_to_be_checked).null_count().alias(
                                         "missing_count"),
                                     pl.col(column_to_be_checked).drop_nulls(
            ).n_unique().alias("unique_count"),
                pl.lit(None).cast(pl.Utf8).alias("mode"),
                pl.lit(list_of_uniq).alias(
                                         "list_of_uniques"),
                pl.lit(rundate).alias("run_date")])

        elif column_type == ColumnType.CATEGORICAL.value:
            mode = self.find_mode_polars(df, column_to_be_checked)
            result_data = df.select([pl.lit(self.job_id).alias("job_id"),
                                     pl.lit(source_type).alias("source_type"),
                                     pl.lit(layer).alias("layer"),
                                     pl.lit(source_name).alias("source_name"),
                                     pl.lit(filename).alias("filename"),
                                     pl.lit(column_to_be_checked).alias(
                                         "column_name"),
                                     pl.lit(column_type).alias("column_type"),
                                     pl.lit(columns).alias(
                                         "total_column_count"),
                                     pl.lit(rows).alias("total_row_count"),
                                     pl.lit(None).cast(pl.Utf8).alias("min"),
                                     pl.lit(None).cast(pl.Utf8).alias("max"),
                                     pl.lit(None).cast(pl.Utf8).alias("avg"),
                                     pl.lit(None).cast(pl.Utf8).alias("sum"),
                                     pl.lit(None).cast(pl.Utf8).alias("stddev"),
                                     pl.lit(None).cast(pl.Utf8).alias("25th_per"),
                                     pl.lit(None).cast(pl.Utf8).alias("50th_per"),
                                     pl.lit(None).cast(pl.Utf8).alias("75th_per"),
                                     pl.col(column_to_be_checked).null_count().alias(
                                         "missing_count"),
                                     pl.col(column_to_be_checked).drop_nulls(
            ).n_unique().alias("unique_count"),
                pl.lit(mode).alias("mode"),
                pl.lit(list_of_uniq).alias(
                                         "list_of_uniques"),
                pl.lit(rundate).alias("run_date")]
            )

        else:
            mode = self.find_mode_polars(df, column_to_be_checked)
            df1 = df.sort(column_to_be_checked)
            result_data = df.select([pl.lit(self.job_id).alias("job_id"),
                                    pl.lit(source_type).alias("source_type"),
                                    pl.lit(layer).alias("layer"),
                                    pl.lit(source_name).alias("source_name"),
                                    pl.lit(filename).alias("filename"),
                                    pl.lit(column_to_be_checked).alias(
                                        "column_name"),
                                    pl.lit(column_type).alias("column_type"),
                                    pl.lit(columns).alias(
                                        "total_column_count"),
                                    pl.lit(rows).alias("total_row_count"),
                                    pl.col(column_to_be_checked).min().cast(
                                        pl.Utf8).alias("min"),
                                    pl.col(column_to_be_checked).max().cast(
                                        pl.Utf8).alias("max"),
                                    pl.lit(None).cast(
                                        pl.Utf8).alias("avg"),
                                    pl.lit(None).cast(
                                        pl.Utf8).alias("sum"),
                                    pl.lit(None).cast(
                                        pl.Utf8).alias("stddev"),
                                     df1[int(-1 * ((0.25 * rows) // -1))-1][column_to_be_checked].cast(
                                         pl.Utf8).alias("25th_per"),
                                     df1[int(-1 * ((0.50 * rows) // -1))-1][column_to_be_checked].cast(
                                         pl.Utf8).alias("50th_per"),
                                     df1[int(-1 * ((0.75 * rows) // -1))-1][column_to_be_checked].cast(
                                         pl.Utf8).alias("75th_per"),
                                    pl.col(column_to_be_checked).null_count().alias(
                                        "missing_count"),
                                    pl.col(column_to_be_checked).drop_nulls(
            ).n_unique().alias("unique_count"),
                pl.lit(mode).alias("mode"),
                pl.lit(list_of_uniq).alias(
                                        "list_of_uniques"),
                pl.lit(rundate).alias("run_date")]
            )
        return result_data

    def find_mode_spark(self, df, column_to_be_checked):
        df = df.filter(col(column_to_be_checked).isNotNull()
                       ).groupBy(column_to_be_checked).count()
        mode_val_count = df.agg(max("count")).take(1)[0][0]
        result = df.filter(col("count") == mode_val_count).select(column_to_be_checked).collect()
        result = [row[column_to_be_checked] for row in result]
        return str(result)

    def find_mode_polars(self, df, column_to_be_checked):
        df = df.filter(pl.col(column_to_be_checked).is_not_null()).groupby(
            column_to_be_checked, maintain_order=True).count()
        mode_val_count = df.select(pl.col("count").max()).item()
        result = df.filter(pl.col("count") == mode_val_count).select(
            pl.col(column_to_be_checked)).get_column(column_to_be_checked).to_list()
        return str(result)

    def list_of_uniques_spark(self, df, column_to_be_checked):
        df = df.filter(col(column_to_be_checked).isNotNull())
        result = df.agg(collect_set(column_to_be_checked)).take(1)[0][0]
        result.sort()
        return str(result[:10])

    def list_of_uniques_polars(self, df, column_to_be_checked):
        df = df.filter(pl.col(column_to_be_checked).is_not_null())
        result = df.select(pl.col(column_to_be_checked)).unique(
        ).get_column(column_to_be_checked).to_list()
        result.sort()
        return str(result[:10])

       # ----- Function takes the filepath of source_csv as an input and apply data profiling.
    def apply_data_profiling(self, source_config_df, write_consolidated_report=True, is_build_dq_rules = False):
        try:
            source_config = source_config_df.rows(named=True)
        except:
            source_config = source_config_df.collect()
        new_tables = get_missing_tables(self.tables_list, source_config)
        self.tables_list = {**self.tables_list, **new_tables}
        new_dataframes = read_dataset(
            new_tables, self.data_read_ob, self.no_of_partition, self.run_engine, True)
        if new_dataframes:
            self.dataframes = {**self.dataframes, **new_dataframes}
        if self.run_engine.lower() == 'polars':
           data_profiling_df = self.apply_data_profiling_to_table_list_polars(
             source_config, write_consolidated_report, is_build_dq_rules)
        else:
           data_profiling_df = self.apply_data_profiling_to_table_list(
             source_config, write_consolidated_report, is_build_dq_rules)
        return data_profiling_df

    def data_profiling_based_quality_rules(self, source_config_df, columns_to_be_excluded):
        try:
            data_profiling_report = self.apply_data_profiling(source_config_df, is_build_dq_rules=True)
            dq_rules_list = self.recommanded_data_quality_rules(data_profiling_report, columns_to_be_excluded)
            return dq_rules_list
        except Exception as e:
            raise Exception(f"Following exception raised while making recommandation data quality rules list: {e}")

    def recommanded_data_quality_rules(self, data_profiling_report, columns_to_be_excluded):    
        try:
            data_quality_rules = []
            if self.run_engine.lower() == 'polars':
                data_profiling_rows = data_profiling_report.rows(named=True)
                # dq_rules_list = self.data_profiling_based_quality_rules_polars(data_profiling_report, columns_to_be_excluded)
            else:
                data_profiling_rows = data_profiling_report.collect()

            data_profiling_rows = sorted(data_profiling_rows, key=operator.itemgetter("source_type","layer", "source_name", "filename"))
            for key, value in itertools.groupby(data_profiling_rows, key= operator.itemgetter("source_type","layer", "source_name", "filename")):
                column_names = ''
                column_types = ''
                date_format_config = {}
                date_formate_dict = ''
                for d_p_r in list(value):
                    # source = f'''{d_p_r["source_type"]}_{d_p_r["layer"]}_{d_p_r["source_name"]}_{d_p_r["filename"]}'''
                    # column_type = column_type_identifier(self.dataframes[source], d_p_r['column_name'], self.run_engine)
                    column_names = f"{column_names},{d_p_r['column_name']}"
                    column_types = f"{column_types},{self.user_column_type(d_p_r['column_type'])}"
                    if d_p_r['column_type'] == ColumnType.DATE.value :
                        date_format_config[d_p_r['column_name']] = 'dd-mm-yyyy'
                        date_formate_dict = "{'dd-mm-yyyy':'%d-%m-%Y'}"
                    if d_p_r['column_name'] not in columns_to_be_excluded:
                        new_rules = self.data_qulity_rule_on_column(d_p_r, d_p_r["column_type"])
                        if len(new_rules) > 0:
                            data_quality_rules.extend(new_rules)
                schema_rule = (d_p_r["container_name"], d_p_r["source_type"], d_p_r["layer"], d_p_r["source_name"],
                d_p_r["filename"], d_p_r["read_connector_method"], 
                "schema_check",column_names.strip(','), column_types.strip(','), str(date_format_config), date_formate_dict, "Mandatory", "1",
                d_p_r["latest_file_path"], d_p_r["output_folder_structure"])
                # print("schema_rule :: ",schema_rule)
                data_quality_rules.append(schema_rule)
            data_quality_rules_df = self.dq_rules_df(data_quality_rules)

            if self.data_right_structure == 'file':
                report_folder_path = f"{data_profiling_rows[0]['output_folder_structure']}{ModuleName.DATAPROFILE.value}/recommanded_data_quality_rules/"
                file_name = f"recommanded_data_quality_rules{datetime.now(self.time_zone).strftime('_%d_%m_%Y_%H_%M_%S')}"
                if self.run_engine.lower() == 'polars':
                    report_path = self.data_write_ob.write_from_polars(data_quality_rules_df, report_folder_path, file_name)
                else:
                    report_path = self.data_write_ob.write(data_quality_rules_df, report_folder_path, file_name)
                print(f"Recommanded data qualty rules report is uploaded successfully at : {report_path}")
            else:
                if self.run_engine.lower() == 'polars':
                    report_path = self.data_write_ob.write_from_polars(data_quality_rules_df, self.output_db_name, 'recommanded_data_quality_rules')
                else:
                    report_path = self.data_write_ob.write(data_quality_rules_df, self.output_db_name, 'recommanded_data_quality_rules')
                print(f"Recommanded data qualty rules report is added successfully at : {report_path}")

            return data_quality_rules_df
        except Exception as e:
            raise Exception(f"Following exception raised while making recommandation data quality rules list: {e}")
    
    def dq_rules_df(self, data_quality_rules):
        if self.run_engine.lower() == 'polars':
            schema = get_schema(QualityCheckConfigStructure.COLUMN_NAME.value, QualityCheckConfigStructure.COLUMN_DATATYPE.value, 'polars')
            data_quality_rules_df = pl.DataFrame(data=data_quality_rules, schema=schema)
        else:
            schema = get_schema(QualityCheckConfigStructure.COLUMN_NAME.value, QualityCheckConfigStructure.COLUMN_DATATYPE.value, 'pyspark')
            data_quality_rules_df = self.spark.createDataFrame(data=data_quality_rules, schema=schema)

        return data_quality_rules_df

    def data_qulity_rule_on_column(self, data_profiling_row, column_type):
        
        new_rules = []
        if data_profiling_row["missing_count"] == 0:
            new_rules.append((data_profiling_row["container_name"], data_profiling_row["source_type"], data_profiling_row["layer"], data_profiling_row["source_name"],
            data_profiling_row["filename"], data_profiling_row["read_connector_method"], 
            "null_check",data_profiling_row["column_name"], "", "", "", "Mandatory", "1",
            data_profiling_row["latest_file_path"], data_profiling_row["output_folder_structure"]))
        if column_type == ColumnType.NUMERICAL.value:
            new_rules.append((data_profiling_row["container_name"], data_profiling_row["source_type"], data_profiling_row["layer"], data_profiling_row["source_name"],
            data_profiling_row["filename"], data_profiling_row["read_connector_method"], 
            "range_min_check",data_profiling_row["column_name"], data_profiling_row["min"], "", "", "Mandatory", "1",
            data_profiling_row["latest_file_path"], data_profiling_row["output_folder_structure"]))
            new_rules.append((data_profiling_row["container_name"], data_profiling_row["source_type"], data_profiling_row["layer"], data_profiling_row["source_name"],
            data_profiling_row["filename"], data_profiling_row["read_connector_method"], 
            "range_max_check",data_profiling_row["column_name"], data_profiling_row["max"], "", "", "Mandatory", "1",
            data_profiling_row["latest_file_path"], data_profiling_row["output_folder_structure"]))
        if column_type == ColumnType.CATEGORICAL.value:
            new_rules.append((data_profiling_row["container_name"], data_profiling_row["source_type"], data_profiling_row["layer"], data_profiling_row["source_name"],
            data_profiling_row["filename"], data_profiling_row["read_connector_method"], 
            "unique_keys_check",data_profiling_row["column_name"], "", "", "", "Mandatory", "1",
            data_profiling_row["latest_file_path"], data_profiling_row["output_folder_structure"]))
            
            new_rules.append((data_profiling_row["container_name"], data_profiling_row["source_type"], data_profiling_row["layer"], data_profiling_row["source_name"],
            data_profiling_row["filename"], data_profiling_row["read_connector_method"], 
            "allowed_values_check",data_profiling_row["column_name"], ','.join(eval(data_profiling_row["mode"])), "", "", "Mandatory", "1",
            data_profiling_row["latest_file_path"], data_profiling_row["output_folder_structure"]))
        if column_type == ColumnType.DATE.value:
            # new_rules.append((data_profiling_row["container_name"], data_profiling_row["source_type"], data_profiling_row["layer"], data_profiling_row["source_name"],
            # data_profiling_row["filename"], data_profiling_row["read_connector_method"], 
            # "range_max_check",data_profiling_row["column_name"], data_profiling_row["max"], "", "", "Mandatory", "1",
            # data_profiling_row["latest_file_path"], data_profiling_row["output_folder_structure"]))
            pass
        new_rules.append((data_profiling_row["container_name"], data_profiling_row["source_type"], data_profiling_row["layer"], data_profiling_row["source_name"],
            data_profiling_row["filename"], data_profiling_row["read_connector_method"], 
            "unique_records_check","", "", "", "", "Mandatory", "1",
            data_profiling_row["latest_file_path"], data_profiling_row["output_folder_structure"]))
        return new_rules

    def user_column_type(self, column_type):
        if column_type == ColumnType.NUMERICAL.value:
            return 'int'
        elif column_type == ColumnType.CATEGORICAL.value:
            return 'string'
        elif column_type == ColumnType.DATE.value:
            return 'date'
        else:
            return 'others'

    def apply_data_profiling_to_table_list(self, source_config, write_consolidated_report, is_build_dq_rules):
        data_profiling_schema = self.data_profiling_schema
        if is_build_dq_rules:
            data_profiling_schema = StructType(data_profiling_schema.fields+[StructField("container_name", StringType(), True),
                                                                             StructField("read_connector_method", StringType(), True),
                                                                             StructField("latest_file_path", StringType(), True),
                                                                             StructField("output_folder_structure", StringType(), True)])
        combined_data_profiling_schema = StructType(data_profiling_schema.fields+[
                                                        StructField("data_profiling_report_write_location", StringType(), True)])
        combined_data_profiling_report_df = self.spark.createDataFrame(
                data=[], schema=combined_data_profiling_schema)
        combined_data_profiling_report_data = []
        for table in source_config:
            try:
                data_profiling_data = []
                source = f'''{table["source_type"]}_{table["layer"]}_{table["source_name"]}_{table["filename"]}'''
                data_profiling_df = self.spark.createDataFrame(
                        data=data_profiling_data, schema=data_profiling_schema)
                self.dataframes[source].cache()
                rows = self.dataframes[source].count()
                columns = len(self.dataframes[source].columns)
                for column in self.dataframes[source].columns:
                    result_df = self.apply_data_profiling_to_column_spark(
                            self.dataframes[source], table["source_type"], table["layer"], table["source_name"], table["filename"], column, rows, columns)
                    if is_build_dq_rules:
                        result_df = result_df.withColumn("container_name", lit(table["container_name"])) \
                            .withColumn("read_connector_method", lit(table["read_connector_method"])) \
                            .withColumn("latest_file_path", lit(table["latest_file_path"])) \
                            .withColumn("output_folder_structure", lit(table["output_folder_structure"]))
                    data_profiling_df = data_profiling_df.union(result_df)
                    
                data_profiling_report_file_path = self.write_data_profiling_report(table, data_profiling_df)
                data_profiling_report_df = data_profiling_df.withColumn(
                        "data_profiling_write_location", lit(data_profiling_report_file_path))
                combined_data_profiling_report_df = combined_data_profiling_report_df.union(
                        data_profiling_report_df)

            except Exception as e:
                rundate = date.today().strftime("%Y/%m/%d")
                data_profiling_report_df = self.spark.createDataFrame(data=[(self.job_id,
                                                                             table["source_type"], table["layer"],
                                                                             table["source_name"], table["filename"],
                                                                             None, None, None, None, None, None, None,
                                                                             None, None, None, None, None, None, None,
                                                                             None, None, lit(rundate),
                                                                             f'Failed to perform profiling, {e}')],
                                                                      schema=combined_data_profiling_schema)
                combined_data_profiling_report_df = combined_data_profiling_report_df.union(
                        data_profiling_report_df)
                continue
        self.write_combined_report(combined_data_profiling_report_df, source_config, write_consolidated_report)
        return combined_data_profiling_report_df
      
    def apply_data_profiling_to_table_list_polars(self, source_config, write_consolidated_report, is_build_dq_rules):
        data_profiling_schema = self.data_profiling_schema
        if is_build_dq_rules: 
            data_profiling_schema = data_profiling_schema + \
                [("container_name", pl.Utf8),("read_connector_method", pl.Utf8),("latest_file_path", pl.Utf8), ("output_folder_structure", pl.Utf8)]
        combined_data_profiling_schema = data_profiling_schema + \
                [("data_profiling_report_write_location", pl.Utf8)]
        combined_data_profiling_report_data = []
        for table in source_config:
            try:
                data_profiling_data = []
                source = f'''{table["source_type"]}_{table["layer"]}_{table["source_name"]}_{table["filename"]}'''
                rows = self.dataframes[source].height
                columns = self.dataframes[source].width
                for column in self.dataframes[source].columns:
                    result_df = self.apply_data_profiling_to_column_polars(self.dataframes[source], table["source_type"], table["layer"], table["source_name"], table["filename"], column, rows, columns)
                    if is_build_dq_rules:
                        result_df = result_df.with_columns([pl.lit(table["container_name"]).alias("container_name"),
                            pl.lit(table["read_connector_method"]).alias("read_connector_method"),
                            pl.lit(table["latest_file_path"]).alias("latest_file_path"),
                            pl.lit(table["output_folder_structure"]).alias("output_folder_structure")
                            ])
                    data_profiling_data = data_profiling_data + result_df.rows()
                data_profiling_df = pl.DataFrame(data=data_profiling_data, schema=data_profiling_schema)
                data_profiling_report_file_path = self.write_data_profiling_report(table, data_profiling_df)
                data_profiling_report_df = data_profiling_df.with_columns(
                        pl.lit(data_profiling_report_file_path).alias("data_profiling_write_location"))
                combined_data_profiling_report_data = combined_data_profiling_report_data + \
                        data_profiling_report_df.rows()
            except Exception as e:
                rundate = date.today().strftime("%Y/%m/%d")
                data_profiling_report_df  = pl.DataFrame(data=[(self.job_id,
                table["source_type"], table["layer"], table["source_name"], table["filename"],
                None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, rundate, f'Failed to perform profiling, {e}')], schema=combined_data_profiling_schema) 
                combined_data_profiling_report_data= combined_data_profiling_report_data + data_profiling_report_df.rows()
                continue
        combined_data_profiling_report_df = pl.DataFrame(data=combined_data_profiling_report_data,
                                                         schema=combined_data_profiling_schema)
        self.write_combined_report(combined_data_profiling_report_df, source_config, write_consolidated_report)
        return combined_data_profiling_report_df
    
    def write_data_profiling_report(self, table, data_profiling_df):
        source = f'''{table["source_type"]}_{table["layer"]}_{table["source_name"]}_{table["filename"]}'''
        if self.data_right_structure == 'file':
            try:
                data_profiling_folder_path = get_folder_structure(
                  table, ModuleName.DATAPROFILE.value)
                
            except Exception as e:
                raise Exception(
                    f"Incorrect folder path or container name not specified, {e}")
                
            data_profiling_file_name = f"data_profiling_report_{source}{datetime.now(self.time_zone).strftime('_%d_%m_%Y_%H_%M_%S')}"
            if self.run_engine.lower() == 'polars':
                data_profiling_report_file_path = self.data_write_ob.write_from_polars(
                    data_profiling_df, data_profiling_folder_path, data_profiling_file_name, table)
            else:
                data_profiling_report_file_path = self.data_write_ob.write(
                    data_profiling_df, data_profiling_folder_path, data_profiling_file_name, table)
            print(f"Data profiling report for {source} is uploaded successfully at : {data_profiling_report_file_path}")
        else:
            if self.run_engine.lower() == 'polars':
                data_profiling_report_file_path = self.data_write_ob.write_from_polars(
                    data_profiling_df, self.output_db_name, source)
            else:
                data_profiling_report_file_path = self.data_write_ob.write(
                    data_profiling_df, self.output_db_name, source)
            print(f"Data profiling report for {source} is added successfully at : {data_profiling_report_file_path}")
        return data_profiling_report_file_path
    
        
    def write_combined_report(self, df, source_config, write_consolidated_report):
        if write_consolidated_report == True:
            if self.data_right_structure == 'file':
                output_report_folder_path = f"{source_config[0]['output_folder_structure']}{ModuleName.DATAPROFILE.value}/consolidated_report/"
                combine_profiling_file_name = f"combined_data_profiling_report_{datetime.now(self.time_zone).strftime('_%d_%m_%Y_%H_%M_%S')}"
                if self.run_engine.lower() == 'polars':
                    combined_data_profiling_report_path = self.data_write_ob.write_from_polars(df,
                                                                                               output_report_folder_path,
                                                                                               combine_profiling_file_name,
                                                                                               source_config[0])
                else:
                    combined_data_profiling_report_path = self.data_write_ob.write(df,
                                                                                   output_report_folder_path,
                                                                                   combine_profiling_file_name,
                                                                                   source_config[0])
                print(f"Combined report is uploaded successfully at : {combined_data_profiling_report_path}")
            else:
                if self.run_engine.lower() == 'polars':
                    combined_data_profiling_report_path=self.data_write_ob.write_from_polars(df,
                                                                                             self.output_db_name,
                                                                                             'combined_data_profiling_report')
                else:
                    combined_data_profiling_report_path=self.data_write_ob.write(df,
                                                                                 self.output_db_name,
                                                                                 'combined_data_profiling_report')
                print(f"Combined report is added successfully at : {combined_data_profiling_report_path}")
        else:
            pass