class RequestHelper:
    def __init__(self, resource):
        self.resource = resource
        self.session = resource.session

    @property
    def schema(self):
        raise NotImplementedError
