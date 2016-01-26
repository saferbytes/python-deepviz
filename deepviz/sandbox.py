import os
import requests
import simplejson
from deepviz.result import ResultError, ResultSuccess

URL_UPLOAD_SAMPLE   = "https://api.deepviz.com/sandbox/submit"
URL_DOWNLOAD_REPORT = "https://api.deepviz.com/general/report"
URL_DOWNLOAD_SAMPLE = "https://api.deepviz.com/sandbox/sample"
URL_DOWNLOAD_BULK   = "https://api.deepviz.com/sandbox/sample/bulk/retrieve"
URL_REQUEST_BULK    = "https://api.deepviz.com/sandbox/sample/bulk/request"


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
            "api_key": api_key,
            "source": "python_deepviz"
        }

        try:
            r = requests.post(
                URL_UPLOAD_SAMPLE,
                data=body,
                files={
                    "file": _file
                }
            )
        except Exception as e:
            msg = "Error while connecting to Deepviz. [%s]" % e
            return ResultError(msg=msg)

        if r.status_code == 200:
            data = simplejson.loads(r.content)
            msg = data['data']
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
            result = self.upload_sample(_file, api_key)
            if result.status == 'error':
                return ResultError(msg="Error uploading file '{file}': {msg}".format(file=_file, msg=result.msg))

            break
        else:
            return ResultSuccess(msg="Every file in folder has been uploaded")

    def download_sample(self, md5=None, path=None, api_key=None):
        if not path or not api_key or not md5:
            msg = "Invalid or missing parameters. Please try again!"
            return ResultError(msg=msg)

        if not os.path.exists(path):
            os.makedirs(path)

        finalpath = os.path.join(path, md5)

        try:
            _file = open(finalpath, "wb")
        except Exception as e:
            msg = "Cannot create file (%s) [%s]" % (finalpath, e)
            return ResultError(msg=msg)

        body = simplejson.dumps(
                {
                    "api_key": api_key,
                    "md5": md5
                })
        try:
            r = requests.post(URL_DOWNLOAD_SAMPLE, data=body)
        except Exception as e:
            msg = "Error while connecting to Deepviz. [%s]" % e
            return ResultError(msg=msg)

        if r.status_code == 200:
            _file.write(r.content)
            _file.close()
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
                "md5": md5,
                "output_filters": ["classification"]
            }
        )
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
                    "md5": md5
                }
            )
        else:
            body = simplejson.dumps(
                {
                    "md5": md5,
                    "api_key": api_key,
                    "output_filters": filters
                }
            )

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

    def bulk_download_request(self, md5_list=None, api_key=None):
        if not md5_list or not api_key:
            msg = "Invalid or missing parameters. Please try again!"
            return ResultError(msg=msg)

        body = simplejson.dumps(
            {
                "api_key": api_key,
                "hashes": md5_list
            })
        try:
            r = requests.post(URL_REQUEST_BULK, data=body)
        except Exception as e:
            msg = "Error while connecting to Deepviz. [%s]" % e
            return ResultError(msg=msg)

        data = simplejson.loads(r.content)

        if r.status_code == 200:
            msg = data['id_request']
            return ResultSuccess(msg="ID request: {id}".format(id=msg))
        else:
            msg = "(%s) Error while connecting to Deepviz. [%s]" % (r.status_code, data['errmsg'])
            return ResultError(msg=msg)

    def bulk_download_retrieve(self, id_request=None, path=None, api_key=None):
        if not path or not api_key or not id_request:
            msg = "Invalid or missing parameters. Please try again!"
            return ResultError(msg=msg)

        if not os.path.exists(path):
            os.makedirs(path)

        finalpath = os.path.join(path, "bulk_request_{id}.zip".format(id=id_request))

        try:
            _file = open(finalpath, "wb")
        except Exception as e:
            msg = "Cannot create file (%s) [%s]" % (finalpath, e)
            return ResultError(msg=msg)

        body = simplejson.dumps(
                {
                    "api_key": api_key,
                    "id_request": str(id_request)
                })
        try:
            r = requests.post(URL_DOWNLOAD_BULK, data=body)
        except Exception as e:
            msg = "Error while connecting to Deepviz. [%s]" % e
            return ResultError(msg=msg)

        if r.status_code == 200:
            _file.write(r.content)
            _file.close()
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