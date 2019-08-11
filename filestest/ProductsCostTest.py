from mks.utility import MksFileSystem as fs
import json
import jsonpath_rw_ext as jp
import logging
import os

folder = fs.get_project_root()
json_plan_file = str(folder) + "\\DocsFolder\\ProductJson\\plan.json"
json_plan_sec_file = str(folder) + "\\DocsFolder\\ProductJson\\prod.json"
json_result_logger = str(folder) + "\\filetest_results\\json_product_diff_logs.log"


with open(json_plan_file) as f:
    plan_data = json.load(f)
with open(json_plan_sec_file) as f1:
    sec_plan_data = json.load(f1)


product_min_path = "$.planCostShares[*].min"
product_max_path = "$.planCostShares[*].max"
product_from_path = "$.planCostShares[*].from"
product_to_path = "$.planCostShares[*].to"
product_scale_path = "$.planCostShares[*].scale"

os.unlink(json_result_logger)
logging.basicConfig(filename=json_result_logger, level=logging.INFO)


def log_comparison(plan_index, global_index, parameter_name):
    pth1 = "$.planCostShares[" + str(plan_index) + "]."+parameter_name
    pth2 = "$.globalcostshares[" + str(global_index) + "]." + parameter_name
    val1, val2 = str(jp.match(pth1, plan_data)), str(jp.match(pth2, sec_plan_data))
    if val1 == val2:
        logging.info("Both files values of " + parameter_name + " is same")
    else:
        logging.error("\t " + parameter_name + " values of file 1 is %s and file 2 is %s", val1, val2)


planCostShares_json_path = "$.planCostShares[*]"
globalCostShares_json_path = "$.globalcostshares[*]"


def get_global_share_values_index(planshare_costsharelevel, planshare_costsharetype, planshare_providertier):

    def find_index(pt):
        sec_index = 0
        for values in jp.match(globalCostShares_json_path, sec_plan_data):
            costsharelevel = str(jp.match("$.globalcostshares[" + str(sec_index) + "].costShareLevel", sec_plan_data))
            costsharetype = str(jp.match("$.globalcostshares[" + str(sec_index) + "].costShareType", sec_plan_data))
            providertier = str(jp.match("$.globalcostshares[" + str(sec_index) + "].providerTier", sec_plan_data))
            if costsharelevel == planshare_costsharelevel and costsharetype == planshare_costsharetype:
                if providertier == pt:
                    return sec_index
        return -1
    my_pt = planshare_providertier
    idx = find_index(my_pt)
    if idx > -1:
        return idx
    else:
        return -1  # "Re-find value with update PT as per document reference" (TO-DO)


index = 0
for values in jp.match(planCostShares_json_path, plan_data):
    logging.info("\n\nProduct dict at position " + str((index + 1)) + "\n==========================================\n")

    ps_costsharelevel = str(jp.match("$.planCostShares[" + str(index) + "].costShareLevel", plan_data))
    ps_costsharetype = str(jp.match("$.planCostShares[" + str(index) + "].costShareType", plan_data))
    ps_providertier = str(jp.match("$.planCostShares[" + str(index) + "].providerTier", plan_data))
    gindex = get_global_share_values_index(ps_costsharelevel, ps_costsharetype, ps_providertier)
    if gindex > -1:
        logging.error("Found matching directory in the prod file at dict position " + str(gindex + 1))
        log_comparison(index, gindex, "min")
        log_comparison(index, gindex, "max")
        log_comparison(index, gindex, "from")
        log_comparison(index, gindex, "to")
        log_comparison(index, gindex, "scale")
    else:
        logging.error("Did not find matching directory in the prod file at all")
    index = index + 1

