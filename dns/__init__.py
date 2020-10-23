from aliyunsdkcore.client import AcsClient
import json
from urllib.request import urlopen
import logging


class DynamicDNS:
    def __init__(self, profile):
        self.client = AcsClient(profile["accessKeyId"], profile["accessKeySecret"], profile["regionId"])

    def describe_domain_records(self, record_type, subdomain):
        logging.info("域名解析记录查询")
        from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
        request = DescribeDomainRecordsRequest()

        request.set_accept_format('json')
        request.set_Type(record_type)
        request.set_DomainName(subdomain)

        response = self.client.do_action_with_exception(request)
        response = str(response, encoding='utf-8')
        result = json.loads(response)
        logging.debug(result)
        return result

    def describe_subdomain_records(self, record_type, subdomain):
        logging.info("子域名解析记录查询")
        from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
        request = DescribeSubDomainRecordsRequest()

        request.set_accept_format('json')
        request.set_Type(record_type)
        request.set_SubDomain(subdomain)

        response = self.client.do_action_with_exception(request)
        response = str(response, encoding='utf-8')
        result = json.loads(response)
        logging.debug(result)
        return result

    def add_record(self, priority, ttl, record_type, value, rr, domain_name):
        logging.info("添加域名解析记录")
        from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
        request = AddDomainRecordRequest()

        request.set_accept_format('json')
        request.set_Priority(priority)
        request.set_TTL(ttl)
        request.set_Value(value)
        request.set_Type(record_type)
        request.set_RR(rr)
        request.set_DomainName(domain_name)

        response = self.client.do_action_with_exception(request)
        response = str(response, encoding='utf-8')
        result = json.loads(response)
        logging.debug(result)
        return result

    def update_record(self, priority, ttl, record_type, value, rr, record_id):
        logging.info("更新域名解析记录")
        from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
        request = UpdateDomainRecordRequest()

        request.set_accept_format('json')
        request.set_Priority(priority)
        request.set_TTL(ttl)
        request.set_Value(value)
        request.set_Type(record_type)
        request.set_RR(rr)
        request.set_RecordId(record_id)

        response = self.client.do_action_with_exception(request)
        response = str(response, encoding='utf-8')
        logging.debug(response)
        return response


class IPManager:
    def __init__(self, file_cache=".ipbuffer"):
        self.ip = ""
        self.file_cache = file_cache

    def get_current_ip(self):
        with urlopen('http://www.3322.org/dyndns/getip') as response:
            self.ip = str(response.read(), encoding='utf-8').replace("\n", "")
            logging.info("current ip: " + self.ip)
        return self.ip

    def sync_cache(self):
        with open(self.file_cache, "w") as f:
            f.write(self.ip)
            logging.info("sync cache ip: " + self.ip)

    def get_cache(self):
        with open(self.file_cache, "r") as f:
            old_ip = f.read()
            logging.info("get cache ip: " + self.ip)
        return old_ip
