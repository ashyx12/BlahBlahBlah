import os
import sys

from blahblahblah.lexer import Lexer
from blahblahblah.parser import Parser
from blahblahblah.semantic import SemanticAnalyzer
from blahblahblah.intermediate import IntermediateGenerator
from blahblahblah.codegen import CodeGenerator


REPORT_DIR = "reports"


def ensure_reports():
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)


def read_input_file(filename):
    with open(filename, "r") as f:
        return f.read()


def create_listing(source, errors):
    lines = source.split("\n")
    listing = []

    for i, line in enumerate(lines, start=1):
        listing.append(f"{i:04d} {line}")
        for err in errors:
            if f"Line {i}:" in err:
                listing.append(f"**** {err}")

    return "\n".join(listing)


def compile(source):

    ensure_reports()

    # ---------- LEXICAL ----------
    lexer = Lexer(source)
    tokens, lex_errors, symbol_table = lexer.tokenize()

    # ---------- PARSER ----------
    parser = Parser(tokens)
    ast = parser.parse_program()

    # ---------- SEMANTIC ----------
    semantic = SemanticAnalyzer()
    semantic_errors = semantic.analyze(ast)

    errors = lex_errors + parser.errors + semantic_errors

    # ---------- LISTING ----------
    listing = create_listing(source, errors)
    with open(f"{REPORT_DIR}/listing.txt", "w") as f:
        f.write(listing)

    # stop if errors
    if errors:
        return

    # ---------- INTERMEDIATE ----------
    icg = IntermediateGenerator()
    intermediate = icg.generate(ast)

    with open(f"{REPORT_DIR}/intermediate_report.txt", "w") as f:
        for line in intermediate:
            f.write(line + "\n")

    # ---------- TARGET ----------
    codegen = CodeGenerator()
    target = codegen.generate(intermediate)

    with open(f"{REPORT_DIR}/target_report.txt", "w") as f:
        for line in target:
            f.write(line + "\n")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python compiler.py <inputfile>")
        sys.exit(1)

    filename = sys.argv[1]
    source = read_input_file(filename)

    compile(source)