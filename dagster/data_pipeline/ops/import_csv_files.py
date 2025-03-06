import os
import tempfile
import clickhouse_connect
from clickhouse_connect.driver.tools import insert_file
from dagster import op

CLICKHOUSE_CONFIG = {"host": "clickhouse", "port": 8123, "username": "default", "password": ""}


@op(required_resource_keys={"global_resource"})
def import_csv_to_clickhouse(context, save_dir: str):
    year, month = context.resources.global_resource.year, context.resources.global_resource.month
    client = clickhouse_connect.get_client(**CLICKHOUSE_CONFIG)
    csv_files = [f for f in os.listdir(save_dir) if f.endswith(".csv")]
    yearmonth_value = f"{year}{month}"

    for file_name in csv_files:
        file_path = os.path.join(save_dir, file_name)
        table_name = os.path.splitext(file_name)[0]
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                column_names = f.readline().strip().replace('"', "").split(",")

            column_definitions = [f'`{col}` Nullable(String)' for col in column_names]
            column_definitions.append("`YearMonth` String") 

            client.command(f"DROP TABLE IF EXISTS STG_{table_name}")
            create_table_sql = f"""
                CREATE TABLE STG_{table_name} (
                    {', '.join(column_definitions)}
                ) ENGINE = MergeTree()
                ORDER BY tuple()
            """
            client.command(create_table_sql)
            context.log.info(f"Table `STG_{table_name}` created.")
        except Exception as e:
            context.log.error(f"Failed to create table `STG_{table_name}`: {e}")

        try:
            with open(
                file_path, "r", encoding="ascii", errors="replace"
            ) as infile, tempfile.NamedTemporaryFile(
                "w", delete=False, encoding="utf-8"
            ) as temp_file:
                next(infile)
                for line in infile:
                    clean_line = line.strip().strip('"')
                    temp_file.write(clean_line + '"' + ',' + '"' + f"{yearmonth_value}\n")
                temp_path = temp_file.name
            
            insert_file(
                client=client,
                table=f"STG_{table_name}",
                file_path=temp_path,
                fmt="CustomSeparated",
                settings={
                    "format_csv_allow_single_quotes": "0",
                    "format_csv_allow_double_quotes": "0",
                    "format_custom_field_delimiter": '","',
                    "format_custom_escaping_rule": "CSV",
                },
            )
            context.log.info(f"Data inserted into `STG_{table_name}`.")
        except Exception as e:
            context.log.error(f"Failed to insert data into `STG_{table_name}`: {e}")