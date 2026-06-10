class HTTPRequest:

    def __init__(self, body, params, query, headers):
        self.body = body
        self.params = params
        self.query = query
        self.headers = headers
