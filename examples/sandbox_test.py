import time
import hashlib
import sys
sys.path.insert(0, r'../')
from deepviz.intel import Intel
from deepviz.sandbox import Sandbox
from deepviz.result import *

API_KEY = "0000000000000000000000000000000000000000000000000000000000000000"

sbx = Sandbox()

# Retrieve sample full scan report
print ">>>>>>>>>>>>>>> sample_report"
result = sbx.sample_report(md5="a6ca3b8c79e1b7e2a6ef046b0702aeb2", api_key=API_KEY)
print result

# Download sample binary
print ">>>>>>>>>>>>>>> download_sample"
print sbx.download_sample(md5="a6ca3b8c79e1b7e2a6ef046b0702aeb2", api_key=API_KEY, path="./")

# Upload sample
print sbx.upload_sample(path="a6ca3b8c79e1b7e2a6ef046b0702aeb2", api_key=API_KEY)

# Upload a folder
result = sbx.upload_folder(path="uploadfolder",  api_key=API_KEY)
print result

# Send a bulk download request and download the related archive
md5_list = [
    "c3bcdbe22836857b1587122adae0f52e",
    "34781d4f8654f9547cc205061221aea5",
    "a8c5c0d39753c97e1ffdfc6b17423dd6"
]

print ">>>>>>>>>>>>>>> bulk_download_request"
result = sbx.bulk_download_request(md5_list=md5_list, api_key=API_KEY)
if result.status == SUCCESS:
    print result
    while True:
        result2 = sbx.bulk_download_retrieve(id_request=result.msg['id_request'], api_key=API_KEY, path=".")
        if result2:
            print result2
            if result2.status != PROCESSING:
                break
        else:
            break
        time.sleep(1)
else:
    print result

#######################################################################################################################

ThreatIntel = Intel()

# sample result
print ">>>>>>>>>>>>>>> sample_result"
result = ThreatIntel.sample_result(md5="a6ca3b8c79e1b7e2a6ef046b0702aeb2", api_key=API_KEY)
print result

# sample info
print ">>>>>>>>>>>>>>> sample_info"
result = ThreatIntel.sample_info(md5="a6ca3b8c79e1b7e2a6ef046b0702aeb2", api_key=API_KEY, filters=["rules", "email", "url", "filesystem"])
print result

# To retrieve intel data about  IPs in the last 7 days:
print ">>>>>>>>>>>>>>> ip_info"
result = ThreatIntel.ip_info(api_key=API_KEY, time_delta="7d")
print result

# To retrieve intel data about one or more IPs:
print ">>>>>>>>>>>>>>> ip_info"
result = ThreatIntel.ip_info(api_key=API_KEY, ip=["216.224.175.0", "216.224.175.250"])
print result

# To retrieve intel data about one or more domains:
print ">>>>>>>>>>>>>>> domain_info"
result = ThreatIntel.domain_info(api_key=API_KEY, domain=["google.com"])
print result

# To retrieve newly registered domains in the last 7 days:
print ">>>>>>>>>>>>>>> domain_info"
result = ThreatIntel.domain_info(api_key=API_KEY, time_delta="10d")
print result

# To run generic search based on strings
# (find all IPs, domains, samples related to the searched keyword):
print ">>>>>>>>>>>>>>> search"
result = ThreatIntel.search(api_key=API_KEY, search_string="google.com")
print result

# To run advanced search based on parameters
# (find all MD5 samples connecting to a domain and determined as malicious):
print ">>>>>>>>>>>>>>> advanced_search"
result = ThreatIntel.advanced_search(api_key=API_KEY, domain=["google.com"], classification="M")
print result

print ">>>>>>>>>>>>>>> advanced_search"
result = ThreatIntel.advanced_search(api_key=API_KEY, ip_range="1.1.1.1-255.255.255.255", classification="M")
print result

# More advanced usage examples
# Find all domains registered in the last 7 days, print out the malware tags related to them and
# list all MD5 samples connecting to them. Then for each one of the samples retrieve the matched
# behavioral rules

result_domains = ThreatIntel.domain_info(api_key=API_KEY, time_delta="3d")
if result_domains.status == SUCCESS:
    domains = result_domains.msg
    for domain in domains.keys():
        result_list_samples = ThreatIntel.advanced_search(api_key=API_KEY, domain=[domain], classification="M")
        if result_list_samples.status == SUCCESS:
            if isinstance(result_list_samples.msg, list):
                if len(domains[domain]['tag']):
                    print "DOMAIN: %s ==> %s samples [TAG: %s]" % (domain, len(result_list_samples.msg), ", ".join((tag for tag in domains[domain]['tag'])))
                else:
                    print "DOMAIN: %s ==> %s samples" % (domain, len(result_list_samples.msg))

                for sample in result_list_samples.msg:
                    result_report = ThreatIntel.sample_info(md5=sample, api_key=API_KEY, filters=["rules"])
                    if result_report.status == SUCCESS:
                        print "%s => [%s]" % (sample, ", ".join([rule for rule in result_report.msg['rules']]))
                    else:
                        print "%s => %s" % (sample, result_report)
                        break
            else:
                print "DOMAIN: %s ==> No samples found" % domain
        else:
            print result_list_samples
            break
else:
    print result_domains