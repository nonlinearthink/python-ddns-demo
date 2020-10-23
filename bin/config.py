#-*- coding: UTF-8 -*-
import os

content = \
"""
# 阿里云配置
# 获取 accessKeyId 和 accessKeySecret: https://help.aliyun.com/knowledge_detail/63482.html
# 获取 regionId: https://help.aliyun.com/document_detail/40654.html
accessKeyId: 
accessKeySecret: 
regionId: 

# 填写你需要绑定的域名
domain:

# log 存储文件
logger: log/ddns.log

# IP 暂存文件
ip_buffer: .ipbuffer
"""

with open("config.yml", "w") as f:
    f.write(content.strip())