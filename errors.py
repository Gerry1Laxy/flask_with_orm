class HttpError(Exception):

    def __init__(self, status_code: int, massage):

        self.status_code = status_code
        self.massage = massage
