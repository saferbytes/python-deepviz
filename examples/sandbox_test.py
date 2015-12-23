from deepviz import sandbox

sbx = sandbox.Sandbox()

result = sbx.sample_result(md5="00000000000000000000000000000000",
                           apikey="0000000000000000000000000000000000000000000000000000000000000000")
f = open("result.txt", "wb")
f.write(str(result))
f.close()

result = sbx.sample_report(md5="00000000000000000000000000000000",
                           apikey="0000000000000000000000000000000000000000000000000000000000000000")
f = open("report.txt", "wb")
f.write(str(result))
f.close()

result = sbx.download_sample(md5="00000000000000000000000000000000",
                             apikey="0000000000000000000000000000000000000000000000000000000000000000", path=".")
