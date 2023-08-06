import requests
import os
import logging
import json
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

def upload_file(data_list,file_name):
    get_current_env()
    url = daemon_network + "/v3/vehicleLogs"
    header = {
        "content-type": "application/x-www-form-urlencoded"
    }

    params = {
        "logDataList": data_list,
        "username": login.get_user_id(),
        "fileName": file_name
    }
    logger.info(f'request url:{url} params:{params}')
    r = requests.post(url, headers=header, data=params)
    logger.info(f"response status_code: {r.status_code} text: {r.text} ")
    if r.status_code == 200:
        result = r.text
        if result == "SUCCESS":
            print("upload success")
        else:
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
