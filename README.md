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

The complete Deepviz REST APIs documentation can be found at https://api.deepviz.com/docs/

# Sandbox SDK API

To upload a sample:

```python
from deepviz import sandbox
sbx = sandbox.Sandbox()
result = sbx.upload_sample(path="path\\to\\file.exe", api_key="my-api-key")
print result
```

To upload a folder:

```python
from deepviz import sandbox
sbx = sandbox.Sandbox()
result = sbx.upload_folder(path="path\\to\\files", api_key="my-api-key")
print result
```

To download a sample:

```python
from deepviz import sandbox
sbx = sandbox.Sandbox()
result = sbx.download_sample(md5="MD5-hash", api_key="my-api-key", path="output\\directory\\")
print result
```

To send a bulk download request and download the related archive:

```python
from deepviz.sandbox import Sandbox
from deepviz.result import *

sbx = Sandbox()
md5_list = [
    "a6ca3b8c79e1b7e2a6ef046b0702aeb2",
    "34781d4f8654f9547cc205061221aea5",
    "a8c5c0d39753c97e1ffdfc6b17423dd6"
]

result = sbx.bulk_download_request(md5_list=md5_list, api_key="my-api-key")
if result.status == SUCCESS:
    print result
    while True:
        result2 = sbx.bulk_download_retrieve(id_request=result.msg['id_request'], api_key="my-api-key", path="output\\directory\\")
        if result2.status != PROCESSING:
            print result2
            break

        time.sleep(1)
```

To retrieve full scan report for a specific MD5

```python
from deepviz import sandbox
sbx = sandbox.Sandbox()
result = sbx.sample_report(md5="MD5-hash", api_key="my-api-key")
print result
```

# Threat Intelligence SDK API

To retrieve scan result of a specific MD5

```python
from deepviz import sandbox
sbx = sandbox.Sandbox()
result = sbx.sample_result(md5="MD5-hash", api_key="my-api-key")
classification = result.msg['classification']

print "Classification: %s" % (classification)
```

To retrieve only specific parts of the report of a specific MD5 scan

```python
from deepviz import sandbox
sbx = sandbox.Sandbox()
result = sbx.sample_report(md5="MD5-hash", api_key="my-api-key", filters=["classification","rules"])
print result
```

To retrieve intel data about an IP:

```python
from deepviz import intel
ThreatIntel = intel.Intel()
result = ThreatIntel.ip_info(api_key="my-api-key", ip="8.8.8.8", filters=["generic_info"])
print result
```

To retrieve intel data about one domain:

```python
from deepviz import intel
ThreatIntel = intel.Intel()
result = ThreatIntel.domain_info(api_key="my-api-key", domain="google.com")
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
