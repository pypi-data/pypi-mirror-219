from .singledatasetqualitycheckpolars import *
from .singledatasetqualitycheckspark import *

class SingleDatasetQualityCheck():

    def __init__(self, tables_list, interaction_between_tables, data_read_ob, data_write_ob, data_right_structure , job_id, time_zone=None, output_db_name="data_quality_output", no_of_partition=4, run_engine = 'pyspark'):
        if run_engine.lower() == 'polars' :
            self.is_run_spark = False
            self.dq_ob = SingleDatasetQualityCheckPolars(tables_list, interaction_between_tables, data_read_ob, data_write_ob, data_right_structure, job_id, time_zone, output_db_name, no_of_partition)
        else:
            self.is_run_spark = True
            self.dq_ob = SingleDatasetQualityCheckSpark(tables_list, interaction_between_tables, data_read_ob, data_write_ob, data_right_structure, job_id, time_zone, output_db_name, no_of_partition)


    def apply_validation(self, rule_config_df, write_summary_on_database = True, failed_schema_source_list = [], output_summary_folder_path='', write_failed_records_flag=True):
        self.dq_ob.apply_validation(rule_config_df, write_summary_on_database, failed_schema_source_list, output_summary_folder_path, write_failed_records_flag)