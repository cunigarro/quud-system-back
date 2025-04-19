class BaseRule:
    def __init__(self):
        self.settings = {}

    def configure(self, settings):
        self.settings = settings

    def execute(self, context):
        raise NotImplementedError

    def save_result(self, data: dict):
        inspection = self.context['inspection']

        for key, value in data.items():
            inspection.result[key] = value

        self.context['db'].commit()
