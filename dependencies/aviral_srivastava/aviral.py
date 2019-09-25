class Aviral:
    def __init__(self, config):
        self.config = config

    def get_name(self, name=None):
        if not name:
            return "Aviral"
        return name

class Sanjay:
    def __init__(self):
        self.child = Aviral("Dad's calling")
        