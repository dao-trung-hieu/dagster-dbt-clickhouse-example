import dagster as dg
from dagster_dbt import dbt_assets, DbtCliResource, DbtProject
from datetime import datetime
import os
import json

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
project_root = os.path.dirname(os.path.dirname(current_dir))
data_transform_path = os.path.join(project_root, "data_transform")

dbt_project = DbtProject(project_dir=data_transform_path)
dbt_resource = DbtCliResource(project_dir=data_transform_path)
dbt_project.prepare_if_dev()

class MyDbtConfig(dg.Config):
    yearmonth: str = datetime.now().strftime("%Y-%m-%d")

@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource, config: MyDbtConfig):
    yearmonth = config.yearmonth
    dbt_vars = {"yearmonth": f"{yearmonth}"}
    context.log.info(f"Running with 'yearmonth': `{dbt_vars}` .")
    dbt_build_args = ["build", "--vars", json.dumps(dbt_vars)]
    yield from dbt.cli(dbt_build_args, context=context).stream()
