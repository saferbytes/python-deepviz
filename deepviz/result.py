SUCCESS = "DEEPVIZ_STATUS_SUCCESS"                  # Request successfully submitted
INPUT_ERROR = "DEEPVIZ_STATUS_INPUT_ERROR"
SERVER_ERROR = "DEEPVIZ_STATUS_SERVER_ERROR"        # Http 5xx
CLIENT_ERROR = "DEEPVIZ_STATUS_CLIENT_ERROR"        # Http 4xx
NETWORK_ERROR = "DEEPVIZ_STATUS_NETWORK_ERROR"      # Cannot contact Deepviz
INTERNAL_ERROR = "DEEPVIZ_STATUS_INTERNAL_ERROR"


class Result:
    status = None
    msg = None

    def __init__(self, status, msg):
        self.status = status
        self.msg = msg

    def __repr__(self):
        return "Result(status='{status}', msg='{data}')".format(status=self.status, data=self.msg)