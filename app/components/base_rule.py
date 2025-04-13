class BaseRule:
    def __init__(self):
        self.settings = {}

    def configure(self, settings):
        self.settings = settings

    def execute(self, context):
        raise NotImplementedError
