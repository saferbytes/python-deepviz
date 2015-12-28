from deepviz import sandbox
import time
import hashlib

API = "0000000000000000000000000000000000000000000000000000000000000000"

sbx = sandbox.Sandbox()

# Retrieve sample scan result
result = sbx.sample_result(md5="00000000000000000000000000000000", api_key=API)
f = open("result.txt", "wb")
f.write(str(result.msg))
f.close()

# Retrieve sample full scan report
result = sbx.sample_report(md5="00000000000000000000000000000000", api_key=API)
f = open("report.txt", "wb")
f.write(str(result.msg))
f.close()

# Download sample binary
sbx.download_sample(md5="00000000000000000000000000000000", api_key=API, path=".")

# Upload sample and wait until the analysis is complete
_hash = hashlib.md5(open("file.exe", 'rb').read()).hexdigest()

sbx.upload_sample(path="file.exe", api_key=API)
result = sbx.sample_result(md5=_hash, api_key=API)

while result.status != "success":
    time.sleep(30)
    result = sbx.sample_result(md5=_hash, api_key=API)

print result.msg['classification']['result']
