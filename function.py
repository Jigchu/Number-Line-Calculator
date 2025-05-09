from expression import Expression

class Function:
    def __init__(self, initialisation: str):
        self.name: int = ""
        self.arg_name: int = ""
        self.expression: Expression
        self.parse(initialisation)

    def parse(self, initialisation: str):
        name, expression = initialisation.split(sep="=")
        expression = "".join(expression)
        self.expression = Expression(expression)

        name, arg_name = name.split(sep="(")
        arg_name = "".join(arg_name)
        self.name = name
        self.arg_name = arg_name.replace(")", "")

    def run(self):
        pass
