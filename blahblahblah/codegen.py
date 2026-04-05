class CodeGenerator:

    def generate(self, intermediate):

        target = []

        for line in intermediate:

            if "=" in line:
                var, val = line.split("=")
                target.append(f"LOAD {val.strip()}")
                target.append(f"STORE {var.strip()}")

            elif line.startswith("READ"):
                target.append("IN " + line.split()[1])

            elif line.startswith("WRITE"):
                target.append("OUT " + line.split()[1])

            else:
                target.append(line)

        return target