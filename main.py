from dns import DynamicDNS, IPManager
import logging
import yaml
from util import check_file


def init():
    # 加载配置文件
    with open("config.yml", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    # 创建日志文件
    check_file(config["logger"])
    # 创建缓存文件
    check_file(config["ip_buffer"])
    # logging 基本设置
    logging.basicConfig(filename=config['logger'], level=logging.DEBUG,
                        format="%(asctime)s  %(filename)s : %(levelname)s  %(message)s", datefmt="%Y-%m-%d %A %H:%M:%S")
    # 同时为 console 创建 logging
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s  %(filename)s : %(levelname)s  %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)
    return config


def main():
    config = init()
    ip_manager = IPManager(config["ip_buffer"])
    profile = {
        "accessKeyId": config["accessKeyId"],
        "accessKeySecret": config["accessKeySecret"],
        "regionId": config["regionId"]
    }
    ddns = DynamicDNS(profile)
    current_ip = ip_manager.get_current_ip()
    if ip_manager.get_cache() == current_ip:
        return
    ip_manager.sync_cache()
    des_result = ddns.describe_domain_records("A", config["domain"])
    print(des_result)
    if des_result["TotalCount"] == 0:
        ddns.add_record("5", "600", "A", current_ip, "www", config["domain"])
    else:
        request_id = des_result["DomainRecords"]["Record"][0]["RecordId"]
        logging.debug("RequestID: " + request_id)
        ddns.update_record("5", "600", "A", current_ip+":5500", "www", request_id)


if __name__ == '__main__':
    main()
