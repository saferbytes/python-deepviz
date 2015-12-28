from deepviz import sandbox
import time
import hashlib

sbx = sandbox.Sandbox()

# Retrieve sample scan result
result = sbx.sample_result(md5="00000000000000000000000000000000",
                           api_key="0000000000000000000000000000000000000000000000000000000000000000")
f = open("result.txt", "wb")
f.write(str(result))
f.close()

# Retrieve sample full scan report
result = sbx.sample_report(md5="00000000000000000000000000000000",
                           api_key="0000000000000000000000000000000000000000000000000000000000000000")
f = open("report.txt", "wb")
f.write(str(result))
f.close()

# Download sample binary
result = sbx.download_sample(md5="00000000000000000000000000000000",
                             api_key="0000000000000000000000000000000000000000000000000000000000000000",
                             path=".")

# Upload a sample and wait until the analysis is complete
_hash = hashlib.md5(open("file.exe", 'rb').read()).hexdigest()

sbx.upload_sample(path="file.exe", api_key="0000000000000000000000000000000000000000000000000000000000000000")
result = sbx.sample_result(md5=_hash, api_key="0000000000000000000000000000000000000000000000000000000000000000")

while result.status != "success":
    time.sleep(30)
    result = sbx.sample_result(md5=_hash, api_key="0000000000000000000000000000000000000000000000000000000000000000")

print result.msg['classification']['result']
