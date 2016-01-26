import inspect
import requests
import simplejson
from deepviz.result import ResultError, ResultSuccess

URL_INTEL_SEARCH            = "https://api.deepviz.com/intel/search"
URL_INTEL_IP                = "https://api.deepviz.com/intel/network/ip"
URL_INTEL_DOMAIN            = "https://api.deepviz.com/intel/network/domain"
URL_INTEL_SEARCH_ADVANCED   = "https://api.deepviz.com/intel/search/advanced"


class Intel:

    def ip_info(self, api_key=None, ip=None, time_delta=None, history=False):
        if not ip and not time_delta and not api_key:
            msg = "Invalid or missing parameters. Please try again!"
            return ResultError(msg=msg)

        if ip and time_delta:
            msg = "You must specify either a list of IPs or timestamp. Please try again!"
            return ResultError(msg=msg)

        if history:
            _history = "true"
        else:
            _history = "false"

        if ip:
            if not isinstance(ip, list):
                msg = "You must provide one or more IPs in a list. Please try again!"
                return ResultError(msg=msg)

            body = simplejson.dumps(
                {
                    "history": _history,
                    "api_key": api_key,
                    "ip": ip,
                }
            )
        elif time_delta:
            body = simplejson.dumps(
                {
                    "time_delta": time_delta,
                    "history": _history,
                    "api_key": api_key,
                }
            )

        try:
            r = requests.post(URL_INTEL_IP, data=body)
        except Exception as e:
            msg = "Error while connecting to Deepviz: (%s)" % e
            return ResultError(msg=msg)

        data = simplejson.loads(r.content)

        if r.status_code == 200:
            msg = data['data']
            return ResultSuccess(msg=msg)
        else:
            msg = "%s - %s" % (r.status_code, data['errmsg'])
            return ResultError(msg=msg)

    def domain_info(self, api_key=None, domain=None, time_delta=None, history=False, filters=None):
        if not domain and not time_delta and not api_key:
            msg = "Invalid or missing parameters. Please try again!"
            return ResultError(msg=msg)

        if domain and time_delta:
            msg = "You must specify either a list of domains or timestamp. Please try again!"
            return ResultError(msg=msg)

        if history:
            _history = "true"
        else:
            _history = "false"

        if filters:
            if not isinstance(filters, list):
                msg = "You must provide one or more output filters in a list. Please try again!"
                return ResultError(msg=msg)

        if domain:
            if not isinstance(domain, list):
                msg = "You must provide one or more IPs in a list. Please try again!"
                return ResultError(msg=msg)

            if filters:
                body = simplejson.dumps(
                    {
                        "output_filters": filters,
                        "history": _history,
                        "api_key": api_key,
                        "domain": domain,
                    }
                )
            else:
                body = simplejson.dumps(
                    {
                        "history": _history,
                        "api_key": api_key,
                        "domain": domain,
                    }
                )

        elif time_delta:
            if filters:
                body = simplejson.dumps(
                    {
                        "output_filters": filters,
                        "time_delta": time_delta,
                        "history": _history,
                        "api_key": api_key,
                    }
                )
            else:
                body = simplejson.dumps(
                    {
                        "time_delta": time_delta,
                        "history": _history,
                        "api_key": api_key,
                    }
                )

        try:
            r = requests.post(URL_INTEL_DOMAIN, data=body)
        except Exception as e:
            msg = "Error while connecting to Deepviz: (%s)" % e
            return ResultError(msg=msg)

        data = simplejson.loads(r.content)

        if r.status_code == 200:
            msg = data['data']
            return ResultSuccess(msg=msg)
        else:
            msg = "%s - %s" % (r.status_code, data['errmsg'])
            return ResultError(msg=msg)

    def search(self, api_key=None, search_string=None, start_offset=None, elements=None):
        if not search_string and not api_key:
            msg = "Invalid or missing parameters. Please try again!"
            return ResultError(msg=msg)

        if start_offset is not None and elements is not None:

            result_set = ["start=%d" % start_offset, "rows=%d" % elements]
            body = simplejson.dumps(
                {
                    "result_set": result_set,
                    "string": search_string,
                    "api_key": api_key,
                }
            )
        else:
            body = simplejson.dumps(
                {
                    "string": search_string,
                    "api_key": api_key,
                }
            )

        try:
            r = requests.post(URL_INTEL_SEARCH, data=body)
        except Exception as e:
            msg = "Error while connecting to Deepviz: %s" % e
            return ResultError(msg=msg)

        data = simplejson.loads(r.content)

        if r.status_code == 200:
            msg = data['data']
            return ResultSuccess(msg=msg)
        else:
            msg = "%s - %s" % (r.status_code, data['errmsg'])
            return ResultError(msg=msg)

    def advanced_search(self,api_key=None, sim_hash=None, created_files=None, imp_hash=None, url=None, strings=None,
                        ip=None, asn=None, classification=None, rules=None, country=None, new_sample=None,
                        time_delta=None, result_set=None, ip_range=None, domain=None):

        if not api_key:
            msg = "Invalid or missing parameters. Please try again!"
            return ResultError(msg=msg)

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
                        msg = "Value '%s' must be in a list form. Please try again!" % i
                        return ResultError(msg=msg)
                else:
                    if isinstance(values[i], str):
                        body[i] = values[i]
                    else:
                        msg = "Value '%s' must be in a string form. Please try again!" % i
                        return ResultError(msg=msg)

        final_body = simplejson.dumps(body)

        try:
            r = requests.post(URL_INTEL_SEARCH_ADVANCED, data=final_body)
        except Exception as e:
            msg = "Error while connecting to Deepviz: %s" % e
            return ResultError(msg=msg)

        data = simplejson.loads(r.content)

        if r.status_code == 200:
            msg = data['data']
            return ResultSuccess(msg=msg)
        else:
            msg = "%s - %s" % (r.status_code, data['errmsg'])
            return ResultError(msg=msg)