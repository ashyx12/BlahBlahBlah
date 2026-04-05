class SemanticAnalyzer:

    def __init__(self):
        self.symbols = set()
        self.errors = []

    def analyze(self, ast):

        _, _, stmts = ast

        for stmt in stmts:

            if stmt[0] == "assign":
                var = stmt[1]
                self.symbols.add(var)

            if stmt[0] == "write":
                var = stmt[1]
                if var not in self.symbols:
                    self.errors.append(f"Semantic error: {var} used before assignment")

            if stmt[0] == "read":
                self.symbols.add(stmt[1])

        # write report
        with open("reports/semantic_report.txt", "w") as f:
            f.write("SYMBOL TABLE\n")
            for s in self.symbols:
                f.write(s + "\n")

            if self.errors:
                f.write("\nERRORS\n")
                for e in self.errors:
                    f.write(e + "\n")

        return self.errors