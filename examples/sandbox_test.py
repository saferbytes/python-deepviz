import time
import hashlib
from deepviz import intel
from deepviz import sandbox

API_KEY = "0000000000000000000000000000000000000000000000000000000000000000"

sbx = sandbox.Sandbox()

# Retrieve sample scan result
result = sbx.sample_result(md5="a6ca3b8c79e1b7e2a6ef046b0702aeb2", api_key=API_KEY)
f = open("result.txt", "wb")
f.write(str(result.msg))
f.close()

# Retrieve sample full scan report
result = sbx.sample_report(md5="a6ca3b8c79e1b7e2a6ef046b0702aeb2", api_key=API_KEY)
f = open("report.txt", "wb")
f.write(str(result.msg))
f.close()

# Download sample binary
print sbx.download_sample(md5="a6ca3b8c79e1b7e2a6ef046b0702aeb2", api_key=API_KEY, path=".")

# Upload sample and wait until the analysis is complete
_hash = hashlib.md5(open("a6ca3b8c79e1b7e2a6ef046b0702aeb2", 'rb').read()).hexdigest()

print sbx.upload_sample(path="a6ca3b8c79e1b7e2a6ef046b0702aeb2", api_key=API_KEY)

result = sbx.sample_result(md5=_hash, api_key=API_KEY)

while result.status != "success":
    time.sleep(30)
    result = sbx.sample_result(md5=_hash, api_key=API_KEY)

print result.msg['classification']['result']

# Send a bulk download request
md5_list = [
    "a6ca3b8c79e1b7e2a6ef046b0702aeb2",
    "34781d4f8654f9547cc205061221aea5",
    "a8c5c0d39753c97e1ffdfc6b17423dd6"
]

result = sbx.bulk_download_request(md5_list=md5_list, api_key=API_KEY)
print result

# Download bulk request archive
print sbx.bulk_download_retrieve(id_request=33, api_key=API_KEY, path=".")

########################################################################################################################

ThreatIntel = intel.Intel()

# To retrieve intel data about  IPs in the last 7 days:
result = ThreatIntel.ip_info(api_key=API_KEY, time_delta="7d")
print result

# To retrieve intel data about one or more IPs:
result = ThreatIntel.ip_info(api_key=API_KEY, ip=["1.22.28.94", "1.23.214.1"])
print result

# To retrieve intel data about one or more domains:
result = ThreatIntel.domain_info(api_key=API_KEY, domain=["google.com"])
print result

# To retrieve newly registered domains in the last 7 days:
result = ThreatIntel.domain_info(api_key=API_KEY, time_delta="7d")
print result

# To run generic search based on strings
# (find all IPs, domains, samples related to the searched keyword):
result = ThreatIntel.search(api_key=API_KEY, search_string="justfacebook.net")
print result

# To run advanced search based on parameters
# (find all MD5 samples connecting to a domain and determined as malicious):
result = ThreatIntel.advanced_search(api_key=API_KEY, domain=["justfacebook.net"], classification="M")
print result

# More advanced usage examples
# Find all domains registered in the last 7 days, print out the malware tags related to them and
# list all MD5 samples connecting to them. Then for each one of the samples retrieve the matched
# behavioral rules

ThreatSbx = sandbox.Sandbox()
result_domains = ThreatIntel.domain_info(api_key=API_KEY, time_delta="7d")
domains = result_domains.msg
for domain in domains.keys():
    result_list_samples = ThreatIntel.advanced_search(api_key=API_KEY, domain=[domain], classification="M")
    if isinstance(result_list_samples.msg, list):
        if len(domains[domain]['tag']):
            print "DOMAIN: %s ==> %s samples [TAG: %s]" % (domain, len(result_list_samples.msg), ", ".join((tag['key'] for tag in domains[domain]['tag'])))
        else:
            print "DOMAIN: %s ==> %s samples" % (domain, len(result_list_samples.msg))
        for sample in result_list_samples.msg:
            result_report = ThreatSbx.sample_report(md5=sample, api_key=API_KEY, filters=["rules"])
            print "%s => [%s]" % (sample, ", ".join((rule for rule in result_report.msg['rules'])))
    else:
        print "DOMAIN: %s ==> No samples found" % domain