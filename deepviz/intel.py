import inspect
import requests
from deepviz.result import *

try:
    import json
except:
    import simplejson as json


URL_INTEL_REPORT            = "https://api.deepviz.com/intel/report"
URL_INTEL_SEARCH            = "https://api.deepviz.com/intel/search"
URL_INTEL_IP                = "https://api.deepviz.com/intel/network/ip"
URL_INTEL_DOMAIN            = "https://api.deepviz.com/intel/network/domain"
URL_INTEL_SEARCH_ADVANCED   = "https://api.deepviz.com/intel/search/advanced"


class Intel:

    def __init__(self):
        pass

    def sample_info(self, md5=None, api_key=None, filters=None):
        if not api_key:
            return Result(status=INPUT_ERROR, msg="API key cannot be null or empty String")

        if not md5:
            return Result(status=INPUT_ERROR, msg="MD5 cannot be null or empty String")

        if not filters:
            return Result(status=INPUT_ERROR, msg="filters cannot be null or empty")

        if len(filters) > 10:
            return Result(status=INPUT_ERROR,  msg="Parameter 'filters' takes at most 10 values ({count} given).".format(count=len(filters)))

        body = json.dumps(
            {
                "md5": md5,
                "api_key": api_key,
                "output_filters": filters
            }
        )

        try:
            r = requests.post(URL_INTEL_REPORT, data=body)
        except Exception as e:
            return Result(status=NETWORK_ERROR, msg="Error while connecting to Deepviz: %s" % e)

        try:
            data = json.loads(r.content)
        except Exception as e:
            return Result(status=INTERNAL_ERROR, msg="Error loading Deepviz response: %s" % e)

        if r.status_code == 428:
            return Result(status=PROCESSING, msg="Analysis is running")
        else:
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
                    return Result(status=CLIENT_ERROR, msg="{status_code} - Client error: {errmsg}".format(status_code=r.status_code, errmsg=data['errmsg']))

    def sample_result(self, md5=None, api_key=None):
        if not api_key:
            return Result(status=INPUT_ERROR, msg="API key cannot be null or empty String")

        if not md5:
            return Result(status=INPUT_ERROR, msg="MD5 cannot be null or empty String")

        return self.sample_info(md5, api_key, ["classification"])

    def ip_info(self, api_key=None, ip=None, filters=None):
        if not api_key:
            return Result(status=INPUT_ERROR, msg="API key cannot be null or empty String")

        if not ip:
            msg = "Parameters missing or invalid. You must specify an IP"
            return Result(status=INPUT_ERROR, msg=msg)

        if not isinstance(ip, str):
            msg = "You must provide the IP in a string"
            return Result(status=INPUT_ERROR, msg=msg)

        if filters is not None:
            if not isinstance(filters, list):
                msg = "You must provide one or more output filters in a list"
                return Result(status=INPUT_ERROR, msg=msg)
            elif not filters:
                msg = "You must provide at least one filter"
                return Result(status=INPUT_ERROR, msg=msg)

        if filters is not None:
            body = json.dumps(
                {
                    "api_key": api_key,
                    "ip": ip,
                    "output_filters": filters
                }
            )
        else:
            body = json.dumps(
                {
                    "api_key": api_key,
                    "ip": ip,
                }
            )

        try:
            r = requests.post(URL_INTEL_IP, data=body)
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
                return Result(status=CLIENT_ERROR, msg="{status_code} - Client error: {errmsg}".format(status_code=r.status_code, errmsg=data['errmsg']))


    def domain_info(self, api_key=None, domain=None, filters=None):
        if not api_key:
            return Result(status=INPUT_ERROR, msg="API key cannot be null or empty String")

        if not domain:
            msg = "Parameters missing or invalid. You must specify a domain"
            return Result(status=INPUT_ERROR, msg=msg)
        elif not isinstance(domain, str):
            msg = "You must provide one a domain in a string"
            return Result(status=INPUT_ERROR, msg=msg)

        if filters is not None:
            if not isinstance(filters, list):
                msg = "You must provide one or more output filters in a list"
                return Result(status=INPUT_ERROR, msg=msg)
            elif not filters:
                msg = "You must provide at least one filter"
                return Result(status=INPUT_ERROR, msg=msg)

        if filters:
            body = json.dumps(
                {
                    "api_key": api_key,
                    "domain": domain,
                    "output_filters": filters,
                }
            )
        else:
            body = json.dumps(
                {
                    "api_key": api_key,
                    "domain": domain,
                }
            )

        try:
            r = requests.post(URL_INTEL_DOMAIN, data=body)
        except Exception as e:
            msg = "Error while connecting to Deepviz: %s" % e
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
                return Result(status=CLIENT_ERROR, msg="{status_code} - Client error: {errmsg}".format(status_code=r.status_code, errmsg=data['errmsg']))


    def search(self, api_key=None, search_string=None, start_offset=None, elements=None):
        if not api_key:
            return Result(status=INPUT_ERROR, msg="API key cannot be null or empty String")

        if not search_string:
            return Result(status=INPUT_ERROR, msg="String to be searched cannot be null or empty")

        if start_offset is not None and elements is not None:
            result_set = ["start=%d" % start_offset, "rows=%d" % elements]
            body = json.dumps(
                {
                    "result_set": result_set,
                    "string": search_string,
                    "api_key": api_key,
                }
            )
        else:
            body = json.dumps(
                {
                    "string": search_string,
                    "api_key": api_key,
                }
            )

        try:
            r = requests.post(URL_INTEL_SEARCH, data=body)
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
                return Result(status=CLIENT_ERROR, msg="{status_code} - Client error: {errmsg}".format(status_code=r.status_code, errmsg=data['errmsg']))


    def advanced_search(self, api_key=None, sim_hash=None, created_files=None, imp_hash=None, url=None, strings=None,
                        ip=None, asn=None, classification=None, rules=None, country=None, never_seen=None,
                        time_delta=None, result_set=None, ip_range=None, domain=None):

        if not api_key:
            return Result(status=INPUT_ERROR, msg="API key cannot be null or empty String")

        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)

        body = {
            'api_key': api_key
        }

        for i in args:
            if values[i] and i != "self" and i != "api_key":
                if i == "sim_hash" or i == "created_files" or i == "imp_hash" or i == "url" or i == "strings" or i == "ip" or i == "asn" or i == "rules" or i == "country" or i == "result_set" or i == "domain":
                    if isinstance(values[i], list):
                        body[i] = values[i]
                    else:
                        msg = "Value '%s' must be in a list form" % i
                        return Result(status=INPUT_ERROR, msg=msg)
                else:
                    if isinstance(values[i], str):
                        body[i] = values[i]
                    else:
                        msg = "Value '%s' must be in a string form" % i
                        return Result(status=INPUT_ERROR, msg=msg)

        final_body = json.dumps(body)

        try:
            r = requests.post(URL_INTEL_SEARCH_ADVANCED, data=final_body)
        except Exception as e:
            return Result(status=NETWORK_ERROR, msg="Error while connecting to Deepviz: %s" % e)

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
                return Result(status=CLIENT_ERROR, msg="{status_code} - Client error: {errmsg}".format(status_code=r.status_code, errmsg=data['errmsg']))