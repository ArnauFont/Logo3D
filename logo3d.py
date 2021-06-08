from antlr4 import *
from logo3dLexer import logo3dLexer
from logo3dParser import logo3dParser
from visitor import EvalVisitor

import sys

if len(sys.argv) == 1:
    print(
        "ERROR: S'esperava un parametre d'arxiu. \nForma correcta python3 logo3d.py test-*.l3d (procediment_inicial [parametres_procediment])")
    sys.exit()

if sys.argv[1] == "help" or sys.argv[1] == "-h":
    print("Per executar logo3d es pot fer:")
    print("1.  python3 logo3d.py --> Per defecte procediment main es l'inicial")
    print("2.  python3 logo3d.py procediment --> Procediment inicial es 'procediment', sense parametres")
    print("3.  python3 logo3d.py procediment p1 p2 p3 ... --> Procediment inicial es 'procediment', amb parametres p1, p2, p3, ...")
    sys.exit()

# Llegim el programa del fitxer indicat per l'usuari
input_stream = FileStream(sys.argv[1])

lexer = logo3dLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = logo3dParser(token_stream)
tree = parser.root()

# print per comprovar que es parseja be el programa
# print(tree.toStringTree(recog=parser))

if len(sys.argv) == 2:
    eval_visitor = EvalVisitor("main", [])
    eval_visitor.visit(tree)
else:
    metode_inici = sys.argv[2]
    i = 3
    args = []
    while i < len(sys.argv):
        args.append(float(sys.argv[i]))
        i += 1
    eval_visitor = EvalVisitor(metode_inici, args)
    eval_visitor.visit(tree)
