# python-deepviz
python-deepviz is a Python wrapper for deepviz.com REST APIs

# Install

python-deepviz is hosted by PyPi

```python
pip install python-deepviz
```

# Usage
To use Deepviz API sdk you will need an API key you can get by
subscribing the service free at https://account.deepviz.com/register/

# Sandbox SDK API

To upload a sample:

```python
from deepviz import sandbox
sbx = sandbox.Sandbox()
sbx.upload_sample(path="path\\to\\file.exe", api_key="my-api-key")
```

To upload a folder:

```python
from deepviz import sandbox
sbx = sandbox.Sandbox()
sbx.upload_folder(path="path\\to\\files", api_key="my-api-key")
```

To download a sample:

```python
from deepviz import sandbox
sbx = sandbox.Sandbox()
sbx.download_sample(md5="MD5-hash", api_key="my-api-key", path="output\\directory\\")
```

To send a bulk download request:

```python
md5_list = [
    "a6ca3b8c79e1b7e2a6ef046b0702aeb2",
    "34781d4f8654f9547cc205061221aea5",
    "a8c5c0d39753c97e1ffdfc6b17423dd6"
]

print sbx.bulk_download_request(md5_list=md5_list, api_key="my-api-key")
```

To download the archive af a bulk download request:

```python
from deepviz import sandbox
sbx = sandbox.Sandbox()
sbx.bulk_download_retrieve(id_request="id-request", api_key="my-api-key", path="output\\directory\\")
```

To retrieve scan result of a specific MD5

```python
from deepviz import sandbox
sbx = sandbox.Sandbox()
result = sbx.sample_result(md5="MD5-hash", api_key="my-api-key")
status = result.msg['classification']['result']
accuracy = result.msg['classification']['accuracy']
print "STATUS: %s ACCURACY: %s" % (status, accuracy)
```

To retrieve full scan report for a specific MD5

```python
from deepviz import sandbox
sbx = sandbox.Sandbox()
result = sbx.sample_report(md5="MD5-hash", api_key="my-api-key")
print result
```

To retrieve only specific parts of the report of a specific MD5 scan

```python
from deepviz import sandbox
sbx = sandbox.Sandbox()
result = sbx.sample_report(md5="MD5-hash", api_key="my-api-key", filters=["classification","rules"])

# List of the optional filters - they can be combined together
# "network_ip",
# "network_ip_tcp",
# "network_ip_udp",
# "rules",
# "classification",
# "created_process",
# "hook_user_mode",
# "strings",
# "created_files",
# "hash",
# "info",
# "code_injection"

print result
```
# Threat Intelligence SDK API

To retrieve intel data about one or more IPs:

```python
from deepviz import intel
ThreatIntel = intel.Intel()
result = ThreatIntel.ip_info(api_key="my-api-key", ip=["1.22.28.94", "1.23.214.1"])
print result
```

To retrieve intel data about IPs contacted in the last 7 days:

```python
from deepviz import intel
ThreatIntel = intel.Intel()
result = ThreatIntel.ip_info(api_key="my-api-key", time_delta="7d")
print result
```

To retrieve intel data about one or more domains:

```python
from deepviz import intel
ThreatIntel = intel.Intel()
result = ThreatIntel.domain_info(api_key="my-api-key", domain=["google.com"], filters=["sub_domains"])

# List of the optional filters - they can be combined together
# "whois",
# "sub_domains"

print result
```

To retrieve newly registered domains in the last 7 days:

```python
from deepviz import intel
ThreatIntel = intel.Intel()
result = ThreatIntel.domain_info(api_key="my-api-key", time_delta="7d", filters=["whois"])

# List of the optional filters - they can be combined together
# "whois",
# "sub_domains"


print result
```

To run generic search based on strings 
(find all IPs, domains, samples related to the searched keyword):

```python
from deepviz import intel
ThreatIntel = intel.Intel()
result = ThreatIntel.search(api_key="my-api-key", search_string="justfacebook.net")
print result
```

To run advanced search based on parameters
(find all MD5 samples connecting to a domain and determined as malicious):

```python
from deepviz import intel
ThreatIntel = intel.Intel()
result = ThreatIntel.advanced_search(api_key="my-api-key", domain=["justfacebook.net"], classification="M")
print result
```

# More advanced usage examples

Find all domains registered in the last 7 days, print out the malware tags related to them and 
list all MD5 samples connecting to them. Then for each one of the samples retrieve the matched
behavioral rules

```python
from deepviz import intel, sandbox
API_KEY="0000000000"
ThreatIntel = intel.Intel()
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
```
result:

```
DOMAIN: avsystemcare.com ==> 8 samples [TAG: trojan.qhost, trojan.rbot, trojan.noupd]
000dde6029443950c8553469887eef9e => [badIpUrlInStrings, suspiciousSectionName, highEntropy, invalidSizeOfCode, invalidPEChecksum, writeExeSections]
2b0a56badf6992af7bbcdfbee7aded4f => [dropExe, antiAv, recentlyRegisteredDomainStrings, autorunRegistryKey, badIpUrlInStrings, runDroppedExe, dialer, sleep, antiDebugging, invalidSizeOfCode, loadImage, runExe, invalidPEChecksum, writeExeSections]
aba074b2373e8ea5661fdafb159c263a => [epOutOfSections, badIpUrlInStrings, invalidSizeOfCode, invalidPEChecksum, epLastSection, writeExeSections]
```