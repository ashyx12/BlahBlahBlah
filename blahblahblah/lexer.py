from dataclasses import dataclass

RESERVED = {
    "and","array","begin","integer","do","else","end",
    "function","if","of","or","not","procedure","program",
    "read","then","var","while","write"
}

DELIMITERS = {
    '(', ')', '[', ']', ';', ':', '.', ',', '*',
    '-', '+', '/', '<', '=', '>'
}

COMPOUND = {"<>",":=","<=",">="}


@dataclass
class Token:
    type: str
    value: str
    line: int


class Lexer:
    def __init__(self, source):
        self.lines = source.split("\n")
        self.tokens = []
        self.errors = []
        self.symbol_table = {}

    def tokenize(self):

        for lineno, line in enumerate(self.lines, start=1):
            self.tokenize_line(line, lineno)

        # write report
        with open("reports/lexer_report.txt", "w") as f:
            f.write("TOKENS\n")
            f.write("------\n")
            for t in self.tokens:
                f.write(f"{t.line}\t{t.type}\t{t.value}\n")

            f.write("\nSYMBOL TABLE\n")
            f.write("------------\n")
            for k in self.symbol_table:
                f.write(f"{k}\n")

            if self.errors:
                f.write("\nERRORS\n")
                for e in self.errors:
                    f.write(e + "\n")

        return self.tokens, self.errors, self.symbol_table

    def tokenize_line(self, line, lineno):

        if "!" in line:
            line = line.split("!")[0]

        i = 0
        while i < len(line):

            ch = line[i]

            if ch.isspace():
                i += 1
                continue

            if ch.isalpha():
                start = i
                while i < len(line) and line[i].isalnum():
                    i += 1
                word = line[start:i].lower()

                if word in RESERVED:
                    self.tokens.append(Token("RESERVED", word, lineno))
                else:
                    self.tokens.append(Token("ID", word[:32], lineno))
                    self.symbol_table[word] = "identifier"
                continue

            if ch.isdigit():
                start = i
                while i < len(line) and line[i].isdigit():
                    i += 1
                self.tokens.append(Token("NUMBER", line[start:i], lineno))
                continue

            if ch == "'":
                i += 1
                string = ""
                while i < len(line) and line[i] != "'":
                    string += line[i]
                    i += 1
                if i >= len(line):
                    self.errors.append(f"Line {lineno}: Unterminated string")
                else:
                    i += 1
                    self.tokens.append(Token("STRING", string, lineno))
                continue

            if i + 1 < len(line):
                two = line[i:i+2]
                if two in COMPOUND:
                    self.tokens.append(Token("SYMBOL", two, lineno))
                    i += 2
                    continue

            if ch in DELIMITERS:
                self.tokens.append(Token("SYMBOL", ch, lineno))
                i += 1
                continue

            self.errors.append(f"Line {lineno}: Invalid character {ch}")
            i += 1