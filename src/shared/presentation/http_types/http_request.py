class HTTPRequest:

    def __init__(self, body, params, query, user_id=None):
        self.body = body
        self.params = params
        self.query = query
        self.user_id = user_id
