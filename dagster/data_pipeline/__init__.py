from datetime import datetime
from dagster import Definitions, ConfigurableResource, job, schedule
from dagster_dbt import build_schedule_from_dbt_selection
from data_pipeline.assets.fetch_csv_link import fetch_csv_links
from data_pipeline.ops.download_csv_files import download_csv_files
from data_pipeline.ops.import_csv_files import import_csv_to_clickhouse
from data_pipeline.ops.run_dbt_model import dbt_resource, dbt_models

@job
def csv_pipeline():
    csv_files = fetch_csv_links()
    save_dir = download_csv_files(csv_files)
    import_csv_to_clickhouse(save_dir)

@schedule(cron_schedule="0 12 * * 1", job=csv_pipeline, execution_timezone="UTC")
def weekly_csv_schedule():
    return {}

weekly_dbt_assets_schedule = build_schedule_from_dbt_selection(
    [dbt_models],
    job_name="dbt_pipeline",
    cron_schedule="0 13 * * 1",
    dbt_select="fqn:*",
)


class GlobalConfig(ConfigurableResource):
    year: str = datetime.now().strftime("%Y")  
    month: str = datetime.now().strftime("%m")

global_resource = GlobalConfig()
defs = Definitions(
    assets=[dbt_models],
    jobs=[csv_pipeline],
    schedules=[weekly_csv_schedule, weekly_dbt_assets_schedule],
    resources={
        "global_resource": global_resource,
        "dbt": dbt_resource,
    },
)