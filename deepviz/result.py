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