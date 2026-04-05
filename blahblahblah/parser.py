class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def expect(self, value):
        tok = self.current()
        if not tok or tok.value != value:
            line = tok.line if tok else "EOF"
            self.errors.append(f"Line {line}: Expected {value}")
        else:
            self.pos += 1

    def parse_program(self):
        self.expect("program")
        name = self.current()
        self.pos += 1
        self.expect(";")

        stmts = []
        while self.current():
            stmt = self.parse_statement()
            if stmt:
                stmts.append(stmt)
            else:
                self.pos += 1

        ast = ("program", name.value, stmts)

        # write report
        with open("reports/parser_report.txt", "w") as f:
            f.write("SYNTAX TREE\n")
            f.write(str(ast) + "\n\n")

            if self.errors:
                f.write("ERRORS\n")
                for e in self.errors:
                    f.write(e + "\n")

        return ast

    def parse_statement(self):
        tok = self.current()
        if not tok:
            return None

        if tok.value == "read":
            self.pos += 1
            self.expect("(")
            var = self.current().value
            self.pos += 1
            self.expect(")")
            return ("read", var)

        if tok.value == "write":
            self.pos += 1
            self.expect("(")
            var = self.current().value
            self.pos += 1
            self.expect(")")
            return ("write", var)

        if tok.type == "ID":
            var = tok.value
            self.pos += 1
            self.expect(":=")
            val = self.current().value
            self.pos += 1
            return ("assign", var, val)

        return None