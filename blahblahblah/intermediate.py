class IntermediateGenerator:

    def generate(self, ast):

        _, _, stmts = ast
        code = []

        for stmt in stmts:

            if stmt[0] == "assign":
                code.append(f"{stmt[1]} = {stmt[2]}")

            if stmt[0] == "read":
                code.append(f"READ {stmt[1]}")

            if stmt[0] == "write":
                code.append(f"WRITE {stmt[1]}")

        return code