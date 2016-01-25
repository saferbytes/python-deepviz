import os
import requests
import simplejson

URL_UPLOAD_SAMPLE = "https://api.deepviz.com/sandbox/submit"
URL_DOWNLOAD_REPORT = "https://api.deepviz.com/general/report"
URL_DOWNLOAD_SAMPLE = "https://api.deepviz.com/sandbox/sample"


class Result:
    status = None
    msg = None

    def __init__(self, status, msg):
        self.status = status
        self.msg = msg

    def __repr__(self):
        return "Result(status='{status}', msg='{data}')".format(status=self.status, data=self.msg)


class ResultError(Result):
    def __init__(self, msg):
        Result.__init__(self, 'error', msg)


class ResultSuccess(Result):
    def __init__(self, msg):
        Result.__init__(self, 'success', msg)


class Sandbox:
    def upload_sample(self, path=None, api_key=None):
        if not path or not api_key:
            msg = "Invalid or missing parameters. Please try again!"
            return ResultError(msg=msg)

        if not os.path.isfile(path):
            msg = "Invalid path or file not found (%s). Please check and try again!" % path
            return ResultError(msg=msg)

        try:
            _file = open(path, "rb")
        except Exception as e:
            msg = "Cannot open file (%s). [%s]" % (path, e)
            return ResultError(msg=msg)

        body = {
            "apikey": api_key,
            "rescan": "false"
        }

        try:
            r = requests.post(
                    URL_UPLOAD_SAMPLE,
                    data=body,
                    files={"file": _file}
            )
        except Exception as e:
            msg = "Error while connecting to Deepviz. [%s]" % e
            return ResultError(msg=msg)

        if r.status_code == 200:
            msg = "File uploaded to Deepviz!"
            return ResultSuccess(msg=msg)
        else:
            try:
                data = simplejson.loads(r.content)
                msg = "Error while connecting to Deepviz. [%s]" % data['errmsg']
                return ResultError(msg=msg)
            except Exception as e:
                data = r.content
                msg = "Error while connecting to Deepviz. [%s]" % data
                return ResultError(msg=msg)

    def upload_folder(self, path=None, api_key=None):
        if not path or not api_key:
            msg = "Invalid or missing parameters. Please try again!"
            return ResultError(msg=msg)

        if not os.path.isdir(path):
            msg = "Path invalid or not found (%s). Please check" % path
            return ResultError(msg=msg)

        buf = os.listdir(path)

        for item in buf:
            _file = os.path.join(path, item)
            print self.upload_sample(_file, api_key)

    def download_sample(self, md5=None, path=None, api_key=None):
        if not path or not api_key or not hash:
            msg = "Invalid or missing parameters. Please try again!"
            return ResultError(msg=msg)

        if not os.path.exists(path):
            os.makedirs(path)

        finalpath = os.path.join(path, md5)

        try:
            file = open(finalpath, "wb")
        except Exception as e:
            msg = "Cannot create file (%s) [%s]" % (finalpath, e)
            return ResultError(msg=msg)

        body = simplejson.dumps(
                {
                    "apikey": api_key,
                    "hash": md5
                })
        try:
            r = requests.post(URL_DOWNLOAD_SAMPLE, data=body)
        except Exception as e:
            msg = "Error while connecting to Deepviz. [%s]" % e
            return ResultError(msg=msg)

        if r.status_code == 200:
            file.write(r.content)
            file.close()
            msg = "File downloaded to %s" % finalpath
            return ResultSuccess(msg=msg)
        else:
            try:
                data = simplejson.loads(r.content)
                msg = "Error while connecting to Deepviz. [%s]" % data['errmsg']
                return ResultError(msg=msg)
            except Exception as e:
                data = r.content
                msg = "Error while connecting to Deepviz. [%s]" % data
                return ResultError(msg=msg)

    def sample_result(self, md5=None, api_key=None):
        if not md5 or not api_key:
            msg = "Invalid or missing parameters. Please try again!"
            return ResultError(msg=msg)

        body = simplejson.dumps(
                {
                    "api_key": api_key,
                    "md5": md5.lower(),
                    "output_filters": ["classification"]
                })
        try:
            r = requests.post(URL_DOWNLOAD_REPORT, data=body)
        except Exception as e:
            msg = "Error while connecting to Deepviz. [%s]" % e
            return ResultError(msg=msg)

        data = simplejson.loads(r.content)

        if r.status_code == 200:
            msg = data['data']
            return ResultSuccess(msg=msg)
        else:
            msg = "(%s) Error while connecting to Deepviz. [%s]" % (r.status_code, data['errmsg'])
            return ResultError(msg=msg)

    def sample_report(self, md5=None, api_key=None, filters=None):
        if not md5 or not api_key:
            msg = "Invalid or missing parameters. Please try again!"
            return ResultError(msg=msg)

        if not filters:
            body = simplejson.dumps(
                    {
                        "api_key": api_key,
                        "md5": md5.lower()
                    })
        else:
            body = simplejson.dumps(
                    {
                        "api_key": api_key,
                        "md5": md5.lower(),
                        "output_filters": filters
                    })

        try:
            r = requests.post(URL_DOWNLOAD_REPORT, data=body)
        except Exception as e:
            msg = "Error while connecting to Deepviz. (%s)" % e
            return ResultError(msg=msg)

        data = simplejson.loads(r.content)

        if r.status_code == 200:
            msg = data['data']
            return ResultSuccess(msg=msg)
        else:
            msg = "(%s) Error while connecting to Deepviz. (%s)" % (r.status_code, data['errmsg'])
            return ResultError(msg=msg)
