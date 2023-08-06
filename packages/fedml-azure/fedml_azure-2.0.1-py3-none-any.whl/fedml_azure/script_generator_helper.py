from .logger import Logger 

class ScriptGeneratorHelper:

    def begin(self, tab="\t"):
        self.code = []
        self.tab = tab
        self.level = 0

    def end(self):
        return ''.join(self.code)

    def write(self, string):
        self.code.append(self.tab * self.level + string)

    def indent(self):
        self.level = self.level + 1

    def dedent(self):
        logger = Logger.get_instance()
        try:
            if self.level == 0:
                raise SyntaxError("internal error in code generator")
            self.level = self.level - 1
        except Exception as e:
            logger.error(e)
            raise