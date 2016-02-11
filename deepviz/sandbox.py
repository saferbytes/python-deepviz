import os
import requests
from deepviz.result import *

try:
    import json
except:
    import simplejson as json

URL_UPLOAD_SAMPLE   = "https://api.deepviz.com/sandbox/submit"
URL_DOWNLOAD_REPORT = "https://api.deepviz.com/general/report"
URL_DOWNLOAD_SAMPLE = "https://api.deepviz.com/sandbox/sample"
URL_DOWNLOAD_BULK   = "https://api.deepviz.com/sandbox/sample/bulk/retrieve"
URL_REQUEST_BULK    = "https://api.deepviz.com/sandbox/sample/bulk/request"


class Sandbox:

    def __init__(self):
        pass

    def upload_sample(self, path=None, api_key=None):
        if not path:
            return Result(status=INPUT_ERROR, msg="File path cannot be null or empty String")

        if not api_key:
            return Result(status=INPUT_ERROR, msg="API key cannot be null or empty String")

        if not os.path.exists(path):
            return Result(status=INPUT_ERROR, msg="File does not exists")

        if os.path.isdir(path):
            return Result(status=INPUT_ERROR, msg="Path is a directory instead of a file")

        try:
            _file = open(path, "rb")
        except Exception as _:
            msg = "Cannot open file '%s'" % path
            return Result(status=INTERNAL_ERROR, msg=msg)

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
            msg = "Error while connecting to Deepviz: %s" % e
            return Result(status=NETWORK_ERROR, msg=msg)

        try:
            data = json.loads(r.content)
        except Exception as e:
            return Result(status=INTERNAL_ERROR, msg="Error loading Deepviz response: %s" % e)

        if r.status_code == 200:
            msg = data['data']
            return Result(status=SUCCESS, msg=msg)
        else:
            if r.status_code >= 500:
                return Result(status=SERVER_ERROR, msg="{status_code} - Error while connecting to Deepviz: {errmsg}".format(status_code=r.status_code, errmsg=data['errmsg']))
            else:
                return Result(status=CLIENT_ERROR, msg="{status_code} - Error while connecting to Deepviz: {errmsg}".format(status_code=r.status_code, errmsg=data['errmsg']))


    def upload_folder(self, path=None, api_key=None):
        if not path:
            return Result(status=INPUT_ERROR, msg="Folder path cannot be null or empty String")

        if not api_key:
            return Result(status=INPUT_ERROR, msg="API key cannot be null or empty String")

        if not os.path.exists(path):
            return Result(status=INPUT_ERROR, msg="Directory does not exists")

        if not os.path.isdir(path):
            return Result(status=INPUT_ERROR, msg="Path is a file instead of a directory")

        buf = os.listdir(path)

        if buf:
            for item in buf:
                _file = os.path.join(path, item)
                result = self.upload_sample(_file, api_key)
                if result.status != SUCCESS:
                    result.msg = "Error uploading file '{file}': {msg}".format(file=_file, msg=result.msg)
                    return result
            else:
                return Result(status=SUCCESS, msg="Every file in folder has been uploaded")
        else:
            return Result(status=INPUT_ERROR, msg="Empty folder")


    def download_sample(self, md5=None, path=None, api_key=None):
        if not path:
            return Result(status=INPUT_ERROR, msg="File path cannot be null or empty String")

        if not api_key:
            return Result(status=INPUT_ERROR, msg="API key cannot be null or empty String")

        if not md5:
            return Result(status=INPUT_ERROR, msg="MD5 cannot be null or empty String")

        if os.path.exists(path) and os.path.isfile(path):
            return Result(status=INPUT_ERROR, msg="Invalid destination folder")
        elif not os.path.exists(path):
            os.makedirs(path)

        finalpath = os.path.join(path, md5)

        try:
            _file = open(finalpath, "wb")
        except Exception as _:
            msg = "Cannot create file '%s'" % finalpath
            return Result(status=INTERNAL_ERROR, msg=msg)

        body = json.dumps(
            {
                "api_key": api_key,
                "md5": md5
            })
        try:
            r = requests.post(URL_DOWNLOAD_SAMPLE, data=body)
        except Exception as e:
            return Result(status=NETWORK_ERROR, msg="Error while connecting to Deepviz: %s" % e)

        if r.status_code == 200:
            _file.write(r.content)
            _file.close()
            return Result(status=SUCCESS, msg="Sample downloaded to '%s'" % finalpath)
        else:
            try:
                data = json.loads(r.content)
            except Exception as e:
                return Result(status=INTERNAL_ERROR, msg="Error loading Deepviz response: %s" % e)

            if r.status_code >= 500:
                return Result(status=SERVER_ERROR, msg="{status_code} - Error while connecting to Deepviz: {errmsg}".format(status_code=r.status_code, errmsg=data['errmsg']))
            else:
                return Result(status=CLIENT_ERROR, msg="{status_code} - Error while connecting to Deepviz: {errmsg}".format(status_code=r.status_code, errmsg=data['errmsg']))


    def sample_result(self, md5=None, api_key=None):
        if not api_key:
            return Result(status=INPUT_ERROR, msg="API key cannot be null or empty String")

        if not md5:
            return Result(status=INPUT_ERROR, msg="MD5 cannot be null or empty String")

        body = json.dumps(
            {
                "api_key": api_key,
                "md5": md5,
                "output_filters": ["classification"]
            }
        )
        try:
            r = requests.post(URL_DOWNLOAD_REPORT, data=body)
        except Exception as e:
            return Result(status=NETWORK_ERROR, msg="Error while connecting to Deepviz: %s" % e)

        try:
            data = json.loads(r.content)
        except Exception as e:
            return Result(status=INTERNAL_ERROR, msg="Error loading Deepviz response: %s" % e)

        if r.status_code == 200:
            return Result(status=SUCCESS, msg=data['data'])
        else:
            if r.status_code >= 500:
                return Result(status=SERVER_ERROR, msg="{status_code} - Error while connecting to Deepviz: {errmsg}".format(status_code=r.status_code, errmsg=data['errmsg']))
            else:
                return Result(status=CLIENT_ERROR, msg="{status_code} - Error while connecting to Deepviz: {errmsg}".format(status_code=r.status_code, errmsg=data['errmsg']))


    def sample_report(self, md5=None, api_key=None, filters=None):
        if not api_key:
            return Result(status=INPUT_ERROR, msg="API key cannot be null or empty String")

        if not md5:
            return Result(status=INPUT_ERROR, msg="MD5 cannot be null or empty String")

        if not filters:
            body = json.dumps(
                {
                    "api_key": api_key,
                    "md5": md5
                }
            )
        else:
            body = json.dumps(
                {
                    "md5": md5,
                    "api_key": api_key,
                    "output_filters": filters
                }
            )

        try:
            r = requests.post(URL_DOWNLOAD_REPORT, data=body)
        except Exception as e:
            return Result(status=NETWORK_ERROR, msg="Error while connecting to Deepviz: %s" % e)

        try:
            data = json.loads(r.content)
        except Exception as e:
            return Result(status=INTERNAL_ERROR, msg="Error loading Deepviz response: %s" % e)

        if r.status_code == 200:
            return Result(status=SUCCESS, msg=data['data'])
        else:
            if r.status_code >= 500:
                return Result(status=SERVER_ERROR, msg="{status_code} - Error while connecting to Deepviz: {errmsg}".format(status_code=r.status_code, errmsg=data['errmsg']))
            else:
                return Result(status=CLIENT_ERROR, msg="{status_code} - Error while connecting to Deepviz: {errmsg}".format(status_code=r.status_code, errmsg=data['errmsg']))


    def bulk_download_request(self, md5_list=None, api_key=None):
        if not api_key:
            return Result(status=INPUT_ERROR, msg="API key cannot be null or empty String")

        if not md5_list:
            return Result(status=INPUT_ERROR, msg="MD5 list empty or invalid")

        body = json.dumps(
            {
                "api_key": api_key,
                "hashes": md5_list
            })
        try:
            r = requests.post(URL_REQUEST_BULK, data=body)
        except Exception as e:
            msg = "Error while connecting to Deepviz. [%s]" % e
            return Result(status=NETWORK_ERROR, msg=msg)

        try:
            data = json.loads(r.content)
        except Exception as e:
            return Result(status=INTERNAL_ERROR, msg="Error loading Deepviz response: %s" % e)

        if r.status_code == 200:
            return Result(status=SUCCESS, msg=data['data'])
        else:
            if r.status_code >= 500:
                return Result(status=SERVER_ERROR, msg="{status_code} - Error while connecting to Deepviz: {errmsg}".format(status_code=r.status_code, errmsg=data['errmsg']))
            else:
                return Result(status=CLIENT_ERROR, msg="{status_code} - Error while connecting to Deepviz: {errmsg}".format(status_code=r.status_code, errmsg=data['errmsg']))


    def bulk_download_retrieve(self, id_request=None, path=None, api_key=None):
        if not path:
            return Result(status=INPUT_ERROR, msg="File path cannot be null or empty String")

        if not api_key:
            return Result(status=INPUT_ERROR, msg="API key cannot be null or empty String")

        if not id_request:
            return Result(status=INPUT_ERROR, msg="Request ID cannot be null or empty String")

        if os.path.exists(path) and os.path.isfile(path):
            return Result(status=INPUT_ERROR, msg="Invalid destination folder")
        elif not os.path.exists(path):
            os.makedirs(path)

        finalpath = os.path.join(path, "bulk_request_{id}.zip".format(id=id_request))

        try:
            _file = open(finalpath, "wb")
        except Exception as _:
            return Result(status=INTERNAL_ERROR, msg="Cannot create file '%s'" % finalpath)

        body = json.dumps(
            {
                "api_key": api_key,
                "id_request": str(id_request)
            })
        try:
            r = requests.post(URL_DOWNLOAD_BULK, data=body)
        except Exception as e:
            _file.close()
            return Result(status=NETWORK_ERROR, msg="Error while connecting to Deepviz: %s" % e)

        if r.status_code == 200:
            _file.write(r.content)
            _file.close()
            return Result(status=SUCCESS, msg="File downloaded to '%s'" % finalpath)
        elif r.status_code == 428:
            _file.close()
            return Result(status=PROCESSING, msg="{status_code} - Your request is being processed. Please try again in a few minutes".format(status_code=r.status_code))
        else:
            _file.close()
            try:
                data = json.loads(r.content)
            except Exception as e:
                return Result(status=INTERNAL_ERROR, msg="Error loading Deepviz response: %s" % e)

            if r.status_code >= 500:
                return Result(status=SERVER_ERROR, msg="{status_code} - Error while connecting to Deepviz: {errmsg}".format(status_code=r.status_code, errmsg=data['errmsg']))
            else:
                return Result(status=CLIENT_ERROR, msg="{status_code} - Error while connecting to Deepviz: {errmsg}".format(status_code=r.status_code, errmsg=data['errmsg']))