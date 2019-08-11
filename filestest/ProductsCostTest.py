from mks.utility import MksFileSystem as fs
import json
import jsonpath_rw_ext as jp
import logging
import os

folder = fs.get_project_root()
json_plan_file = str(folder) + "\\DocsFolder\\ProductJson\\plan.json"
json_plan_sec_file = str(
    folder) + "\\DocsFolder\\ProductJson\\plan_IN-LG-RX T Ded20%30% (PrevRX at Zero Cost Share) (23876).json"
json_result_logger = str(folder) + "\\filetest_results\\json_product_diff_logs.log"


with open(json_plan_file) as f:
    plan_data = json.load(f)
with open(json_plan_sec_file) as f1:
    sec_plan_data = json.load(f1)


products_list_path = "$.planCostShares[*]"
product_min_path = "$.planCostShares[*].min"
product_max_path = "$.planCostShares[*].max"
product_from_path = "$.planCostShares[*].from"
product_to_path = "$.planCostShares[*].to"
product_scale_path = "$.planCostShares[*].scale"

os.unlink(json_result_logger)
logging.basicConfig(filename=json_result_logger, level=logging.INFO)


def log_comparison(product_index, parameter_name):
    pth = "$.planCostShares[" + str(product_index) + "]."+parameter_name
    val1, val2 = str(jp.match(pth, plan_data)), str(jp.match(pth, sec_plan_data))
    if val1 == val2:
        logging.info("Both files values of " + parameter_name + " is same")
    else:
        logging.error("\t " + parameter_name + " values of file 1 is %s and file 2 is %s", val1, val2)


index = 0
for values in jp.match(products_list_path, plan_data):
    logging.info("\n\nProduct set at position " + str((index + 1)) + "\n==========================================\n")
    log_comparison(index, "min")
    log_comparison(index, "max")
    log_comparison(index, "from")
    log_comparison(index, "to")
    log_comparison(index, "scale")
    index = index + 1
