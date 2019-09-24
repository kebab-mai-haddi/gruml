import aviral


class Srivastava:
    def __init__(self, config):
        self.config = config

    def get_config(self):
        ob = aviral.Aviral(self.config)
        return ob.get_name("Srivastava")
