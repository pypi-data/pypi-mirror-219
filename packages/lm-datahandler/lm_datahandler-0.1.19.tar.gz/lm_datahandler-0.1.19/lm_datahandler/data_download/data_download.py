import json
import requests
import os


def download_lm_data_from_server(params, data_save_path):
    assert data_save_path is not None, "Data save path should not be none."

    download_url = 'http://8.136.42.241:38083/inner/filter'

    response = requests.post(download_url, data=json.dumps(params), headers={'Content-Type': 'application/json'})

    data_infos = json.loads(response.text)

    if not os.path.exists(data_save_path):
        os.makedirs(data_save_path)

    result_list = []

    for data_info in data_infos:
        data_info["recordStartDate"] = data_info["recordStartDate"][0:8] + "_" + data_info["recordStartDate"][
                                                                                 9:11] + "_" + data_info[
                                                                                                   "recordStartDate"][
                                                                                               12:14] + "_" + data_info[
                                                                                                                  "recordStartDate"][
                                                                                                              15:17]
        data_info["recordEndDate"] = data_info["recordEndDate"][0:8] + "_" + data_info["recordEndDate"][9:11] + "_" + \
                                     data_info["recordEndDate"][12:14] + "_" + data_info["recordEndDate"][15:17]
        dir_name = str(data_info["phone"]) + "_" + data_info["recordStartDate"] + "_" + data_info["recordEndDate"]
        data_path = os.path.join(data_save_path, dir_name)
        if os.path.exists(data_path):
            continue
        os.makedirs(data_path)
        result_list.append(dir_name)
        print("downloading data: " + dir_name)

        oss_path_dict = {
            "eeg.eeg": data_info["eegData"] if 'eegData' in data_info else '',
            "acc.acc": data_info["accData"] if 'accData' in data_info else '',
            "emg.emg": data_info["emgData"] if 'emgData' in data_info else '',
            "sti.sti": data_info["stiData"] if 'stiData' in data_info else '',
            "n3.log": data_info["n3LogData"] if 'n3LogData' in data_info else '',
            "sti.log": data_info["stiLogData"] if 'stiLogData' in data_info else '',
            "ble.ble": data_info["bleData"] if 'bleData' in data_info else '',
            "light.light": data_info['lightData'] if 'lightData' in data_info else ''
        }
        for k in oss_path_dict:
            v = oss_path_dict[k]
            if v is not None and v != '':
                response = requests.get(v)
                with open(data_path + "/" + k, 'wb') as f:
                    f.write(response.content)
                print("file download finish: " + dir_name + "/" + k)
        with open(data_path + "/sleep_analyse.txt", 'w') as f:
            json.dump(data_info, f)

    return result_list
