class BaseRule:
    def __init__(self):
        self.settings = {}

    def configure(self, settings):
        self.settings = settings

    def execute(self, context):
        raise NotImplementedError

    def save_inspection(self, data: dict):
        inspection = self.context['inspection']

        for key, value in data.items():
            inspection[key] = value

        self.context['db'].commit()
