from mks.utility import MksFileSystem as fs
import json
import jsonpath_rw_ext as jp

folder = fs.get_project_root()
json_plan_file = str(folder) + "\\DocsFolder\\ProductJson\\ProviderTierMapping.json"


def get_providertier_values(key):
    with open(json_plan_file) as f:
        plan_data = json.load(f)
    try:
        return plan_data[key]
    except:
        return None


def find_index(file_json_data, planshare_costsharelevel, planshare_costsharetype, planshare_providertier):
    globalCostShares_json_path = "$.globalcostshares[*]"
    sec_index = 0
    for values in jp.match(globalCostShares_json_path, file_json_data):
        costsharelevel = jp.match("$.globalcostshares[" + str(sec_index) + "].costShareLevel", file_json_data)[0]
        costsharetype = jp.match("$.globalcostshares[" + str(sec_index) + "].costShareType", file_json_data)[0]
        providertier = jp.match("$.globalcostshares[" + str(sec_index) + "].providerTier", file_json_data)[0]

        if costsharelevel == planshare_costsharelevel and costsharetype == planshare_costsharetype:
            if providertier == planshare_providertier:
                return sec_index
        sec_index = sec_index + 1
    return -1


def get_global_share_values_index(file_json_data, planshare_costsharelevel, planshare_costsharetype, planshare_providertier):

    tier_values = get_providertier_values(planshare_providertier)
    if tier_values is not None:
        for psp in tier_values:
            idx = find_index(file_json_data, planshare_costsharelevel, planshare_costsharetype, psp)
            if idx > -1:
                return idx
            else:
                idx = -1
    else:
        raise ValueError("There is no provider tier key " + planshare_providertier + "found in the "
                                                                                     "ProvidertierMapping.json file")
    return idx
