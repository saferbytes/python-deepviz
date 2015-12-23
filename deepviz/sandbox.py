import requests
import os
import simplejson

URL_UPLOAD_SAMPLE = "https://api.deepviz.com/sandbox/submit"
URL_DOWNLOAD_REPORT = "https://api.deepviz.com/general/report"
URL_DOWNLOAD_SAMPLE = "https://api.deepviz.com/sandbox/sample"


class Sandbox(object):
    def upload_sample(self, path=None, apikey=None, rescan=False):
        if not path or not apikey:
            return "[ERROR] Invalid or missing parameters. Please try again!"

        if not os.path.isfile(path):
            return "[ERROR] Path invalid or file not found. Please check"

        try:
            file = open(path, "rb")
        except Exception as e:
            return "[ERROR] Cannot open file. (%s)" % e

        try:
            if rescan:
                _rescan = "true"
            else:
                _rescan = "false"

            r = requests.post(
                    URL_UPLOAD_SAMPLE,
                    data=simplejson.dumps({
                        "apikey": apikey,
                        "rescan": _rescan
                    }),

                    files={"file": file}
            )
        except Exception as e:
            return "[ERROR] Error while connecting to Deepviz. (%s)" % e

        if r.status_code == 200:
            return "[SUCCESS] File uploaded to Deepviz!"
        else:
            data = simplejson.loads(r.content)
            return "[ERROR] Error while connecting to Deepviz. (%s)" % data['errmsg']

    def upload_folder(self, path=None, apikey=None, rescan=False):
        if not path or not apikey:
            return "[ERROR] Invalid or missing parameters. Please try again!"

        if not os.path.isdir(path):
            return "[ERROR] Path invalid or not found. Please check"

        buf = os.listdir(path)

        for item in buf:
            file = os.path.join(path, item)
            print Sandbox.upload_sample(file, apikey, rescan)

    def download_sample(self, md5=None, path=None, apikey=None, rescan=False):
        if not path or not apikey or not hash:
            return "[ERROR] Invalid or missing parameters. Please try again!"

        if not os.path.exists(path):
            os.makedirs(path)

        finalpath = os.path.join(path, md5)

        try:
            file = open(finalpath, "wb")
        except Exception as e:
            return "[ERROR] Cannot create file. (%s)" % e

        body = simplejson.dumps(
                {
                    "apikey": apikey,
                    "hash": md5
                })
        try:
            r = requests.post(URL_DOWNLOAD_SAMPLE, data=body)
        except Exception as e:
            return "[ERROR] Error while connecting to Deepviz. (%s)" % e

        if r.status_code == 200:
            file.write(r.content)
            file.close()
            return "[SUCCESS] File downloaded to %s" % finalpath
        else:
            data = simplejson.loads(r.content)
            return "[ERROR] Error while connecting to Deepviz. (%s)" % data['errmsg']

    def sample_result(self, md5=None, apikey=None):
        if not md5 or not apikey:
            return "[ERROR] Invalid or missing parameters. Please try again!"

        try:
            r = requests.post(
                    URL_DOWNLOAD_REPORT,
                    data=simplejson.dumps({
                        "api_key": apikey,
                        "md5": md5,
                        "output_filters": ["classification"]
                    })
            )
        except Exception as e:
            return "[ERROR] Error while connecting to Deepviz. (%s)" % e

        data = simplejson.loads(r.content)

        if r.status_code == 200:
            return data['data']
        else:
            return "[ERROR] (%s) Error while connecting to Deepviz. (%s)" % (r.status_code, data['errmsg'])

    def sample_report(self, md5=None, apikey=None, filters=None):
        if not md5 or not apikey:
            return "[ERROR] Invalid or missing parameters. Please try again!"

        if not filters:
            body = simplejson.dumps(
                    {
                        "api_key": apikey,
                        "md5": md5
                    })
        else:
            body = simplejson.dumps(
                    {
                        "api_key": apikey,
                        "md5": md5,
                        "output_filters": filters
                    })

        try:
            r = requests.post(URL_DOWNLOAD_REPORT, data=body)
        except Exception as e:
            return "[ERROR] Error while connecting to Deepviz. (%s)" % e

        data = simplejson.loads(r.content)

        if r.status_code == 200:
            return data['data']
        else:
            return "[ERROR] (%s) Error while connecting to Deepviz. (%s)" % (r.status_code, data['errmsg'])