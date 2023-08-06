import sys
from os.path import abspath, dirname

dir_above = dirname(dirname(abspath(__file__)))
sys.path.insert(0, dir_above)

from npgbq import NPGBQ
# ref: https://github.com/googleapis/python-bigquery-datatransfer/blob/main/samples/snippets/manage_transfer_configs.py
PROJECT_ID = "cto-cds-datamart-hub-dev"
SQL = "CALL `cto-cds-datamart-hub-dev.ECOM_DATA_MODEL.SP_DATA_MODEL_REFRESH_DAILY`();"
location = "asia-southeast1"

# for create or update
dataset_id = ""
display_name = "DEV_NP"
service_account_name = "bi-models-dev@cto-cds-datamart-hub-dev.iam.gserviceaccount.com"

def get_target_names(display_name,data):
    res = []
    for d in data:
        if display_name == d['display_name']:
            res.append(d['name'])
    return res


if __name__ == "__main__":
    gbq = NPGBQ(project_id=PROJECT_ID)
    data = gbq.list_configs(project_id=PROJECT_ID, location=location)
    gbq.create_config(
        project_id=PROJECT_ID,
        location=location,
        sql=SQL,
        dataset_id=dataset_id,
        display_name=display_name,
        service_account_name=service_account_name,
    )
    data = gbq.list_configs(project_id=PROJECT_ID, location=location)
    names = get_target_names(display_name,data)
    for name in names:
        gbq.delete_config(name=name)

