# python-deepviz
python-deepviz is a wrapper for deepviz.com REST APIs

# Usage

To use Deepviz API sdk you will need an API key you can get by
subscribing the service free at https://account.deepviz.com/register/

# Sandbox SDK API

To upload a sample:

```python
from deepviz import sandbox

sbx = sandbox.Sandbox()
sbx.upload_sample(path="path\\to\\file.exe", apikey="my-api-key")
```

To upload a folder:

```python
from deepviz import sandbox

sbx = sandbox.Sandbox()
sbx.upload_folder(path="path\\to\\files", apikey="my-api-key")
```

To download a sample:

```python
from deepviz import sandbox

sbx = sandbox.Sandbox()
sbx.download_sample(hash="MD5-hash", apikey="my-api-key", path="output\\directory\\")
```

To retrieve scan result of a specific MD5

```python
from deepviz import sandbox

sbx = sandbox.Sandbox()
result = sbx.sample_result(md5="MD5-hash", apikey="my-api-key")

status = result['classification']['result']
accuracy = result['classification']['accuracy']
print "STATUS: %s ACCURACY: %s" % (status, accuracy)
```

To retrieve full scan report for a specific MD5

```python
from deepviz import sandbox

sbx = sandbox.Sandbox()
result = sbx.sample_report(md5="MD5-hash", apikey="my-api-key")
print result
```

To retrieve only specific parts of the report of a specific MD5 scan

```python
from deepviz import sandbox

sbx = sandbox.Sandbox()
result = sbx.sample_report(md5="MD5-hash", apikey="my-api-key", filters=["classification","rules"])

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
