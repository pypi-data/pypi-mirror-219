import requests
import os
import logging
import json
from tqdm import tqdm
from start import utils,login


daemon_network = "https://nvos-toolchain.nioint.com"

daemon_network_mapping = {
    "prod": "https://sky-eye-trace.nioint.com",
    "stg": "https://sky-eye-trace-stg.nioint.com",
    "dev": "https://sky-eye-trace-dev.nioint.com",
    "local": "http://127.0.0.1:12800"
}

daemon_network_front_mapping = {
    "prod": "https://ndtc.nioint.com/#/nvosTool/spaceList",
    "stg": "https://ndtc-stg.nioint.com/#/nvosTool/spaceList",
    "dev": "https://soa-tools-dev.nioint.com/#/nvosTool/spaceList",
    "local": "http://127.0.0.1:12800"
}

# 导入全局日志记录器
logger = logging.getLogger(__name__)

global_var = 0

exist_error = False

def upload_file_process(data_list,fileName):
    global global_var
    global exist_error
    total = int((len(data_list) / 1000) + 1)
    with tqdm(desc="uploading", total= total) as progress:
        for index in range(0, total):
            temp_list = data_list[index * 1000: (index + 1) * 1000]
            upload_file(temp_list,fileName,index)
            progress.update(1)




def upload_file(data_list,file_name,index):
    global global_var
    global exist_error
    get_current_env()
    url = daemon_network + "/v3/vehicleLogs"
    header = {
        "content-type": "application/x-www-form-urlencoded"
    }

    params = {
        "logDataList": data_list,
        "username": login.get_user_id(),
        "fileName": file_name,
        "index": index
    }
    logger.info(f'request url:{url} params:{params}')
    r = requests.post(url, headers=header, data=params)
    logger.info(f"response status_code: {r.status_code} text: {r.text} ")
    if r.status_code == 200:
        result = r.text
        if result == "SUCCESS":
            global_var = global_var + 1
        else:
            exist_error = True
            print("upload fail ,Please try again later.")
    return {}



def get_current_env():
    global daemon_network
    result = {}
    if os.path.exists(os.path.expanduser(os.path.join('~', '.ndtcrc', 'skyeye_env'))):
        with open(os.path.expanduser(os.path.join('~', '.ndtcrc', 'skyeye_env')), 'r')as f:
            result = json.loads(f.readline().strip())
            daemon_network = result["cloud"]
            tip = result["tip"]
            env = result["env"]
            logger.info(f"current env:{env} this cloud linked:{tip} daemon_network:{daemon_network}")
    if result == {}:
        result["cloud"] = daemon_network_mapping.get('prod')
        result['env'] = 'prod'
        result['tip'] = daemon_network_front_mapping.get('prod')
    return result


def switch_env(env):
    val = daemon_network_mapping.get(env)
    if len(val) == 0:
        return
    tip = daemon_network_front_mapping.get(env)
    result = {"cloud":val,"tip":tip,"env":env}
    utils.check_local_workspace()
    with open(os.path.expanduser(os.path.join('~','.ndtcrc' ,'skyeye_env')), 'w') as f:
        f.writelines(json.dumps(result))
    print(f"this script current env:{env} and cloud linked:{tip}")
