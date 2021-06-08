from turtle3d import Turtle3D


if __name__ is not None and "." in __name__:
    from .logo3dParser import logo3dParser
    from .logo3dVisitor import logo3dVisitor
else:
    from logo3dParser import logo3dParser
    from logo3dVisitor import logo3dVisitor


class EvalVisitor(logo3dVisitor):

    def __init__(self, procediment_inici, parametres) -> None:
        self.pila_taules = []
        self.taula_valors = {}
        self.dic_funcions = {}
        self.params = parametres
        self.primer_procediment = procediment_inici
        self.turtle = Turtle3D()
        super().__init__()

    def __comprovaRepetits(self, nom_proc, params):
        set_params = set(params)
        if len(set_params) != len(params):
            raise NameError("Parametres repetits en procediment " + nom_proc)

    def visitRoot(self, ctx):
        l = list(ctx.getChildren())
        # cada fill es una funcio
        for i in range(len(l)-1):
            name = str(l[i].getText())
            name = name.split('(')[0][4:]
            blacklist = ["forward", "backward", "left", "right",
                         "up", "down", "show", "hide", "color", "home"]
            if name in blacklist:
                raise NameError("El metode " + name +
                                " esta reservat per la classe Turtle3D")
            else:
                if self.dic_funcions.get(name):
                    raise NameError("Procediment " + name +
                                    " ja ha estat definit")
                else:
                    self.dic_funcions[name] = l[i]
        if self.dic_funcions.get(self.primer_procediment):
            self.visit(self.dic_funcions[self.primer_procediment])
        else:
            raise NameError("Procediment " +
                            self.primer_procediment + " no declarat.")

    def visitFunc(self, ctx):
        l = list(ctx.getChildren())
        self.taula_valors = {}
        parametres = self.visit(l[2])
        # self.params te la llista amb el valor dels parametres
        # params es la llista amb els noms del parametres
        self.__comprovaRepetits(l[1].getText(), parametres)
        if len(self.params) != len(parametres):
            raise NameError("Parametres per procediment " +
                            l[1].getText() + " incorrectes.")
        for i in range(len(self.params)):
            self.taula_valors[parametres[i]] = self.params[i]
        return self.visitChildren(ctx)

    def visitParams(self, ctx):
        l = list(ctx.getChildren())
        if len(l) == 2:
            return []
        else:
            params = []
            for i in range(1, len(l), 2):
                params.append(self.visit(l[i]))
            return params

    def visitParamsFunc(self, ctx):
        l = list(ctx.getChildren())
        if len(l) == 2:
            return []
        else:
            params = []
            for i in range(1, len(l), 2):
                params.append(l[i].getText())
            return params

    # Assignacio

    def visitAssignacio(self, ctx):
        l = list(ctx.getChildren())
        self.taula_valors[l[0].getText()] = self.visit(l[2])

    # Read

    def visitRead(self, ctx):
        l = list(ctx.getChildren())
        var = float(input(l[1].getText() + ": "))
        self.taula_valors[l[1].getText()] = var

    # Write

    def visitWrite(self, ctx):
        l = list(ctx.getChildren())
        print(self.visit(l[1]))

    # Condicional
    def visitCondicional(self, ctx):
        l = list(ctx.getChildren())
        if(self.visit(l[1])):
            for i in range(3, len(l)-1):
                self.visit(l[i])

    # CondicionalElse

    def visitCondicionalElse(self, ctx):
        l = list(ctx.getChildren())
        if(self.visit(l[1])):
            i = 3
            while i < len(l) and l[i].getText() != 'ELSE':
                # print("inside if: "+l[i].getText())
                self.visit(l[i])
                i += 1
        else:
            i = 3
            while i < len(l) and l[i].getText() != 'ELSE':
                # print("skipping: "+ l[i].getText())
                i += 1
            i += 1
            while i < len(l)-1:
                # print("inside else: "+l[i].getText())
                self.visit(l[i])
                i += 1

    # While

    def visitWhile(self, ctx):
        l = list(ctx.getChildren())
        while(self.visit(l[1])):
            i = 3
            while(l[i].getText() != 'END'):
                self.visit(l[i])
                i += 1
    # For

    def visitFor(self, ctx):
        l = list(ctx.getChildren())

        var = l[1].getText()
        init = self.visit(l[3])
        self.taula_valors[var] = init

        end = self.visit(l[5])

        while self.taula_valors[var] <= end:
            i = 7
            while i < len(l) and l[i].getText() != 'END':
                self.visit(l[i])
                i += 1
            self.taula_valors[var] += 1

    # Expresio
    def visitExpr(self, ctx):
        l = list(ctx.getChildren())
        if len(l) == 1:
            if l[0].getText().isdigit():
                return float(l[0].getText())
            elif self.taula_valors.get(l[0].getText()):
                return self.taula_valors[l[0].getText()]
            else:
                return float(0)
        elif len(l) == 2:  # es tracta d'una crida a un procediment
            nom_procediment = l[0].getText()
            if self.dic_funcions.get(nom_procediment):
                self.params = self.visit(l[1])
                self.pila_taules.append(self.taula_valors)
                self.visit(self.dic_funcions[nom_procediment])
                self.taula_valors = self.pila_taules.pop()
                return 0
            else:
                params = self.visit(l[1])
                if nom_procediment == "forward":
                    self.turtle.forward(params[0])
                    return 0
                elif nom_procediment == "backward":
                    self.turtle.backward(params[0])
                    return 0
                elif nom_procediment == "left":
                    self.turtle.left(params[0])
                    return 0
                elif nom_procediment == "right":
                    self.turtle.right(params[0])
                    return 0
                elif nom_procediment == "up":
                    self.turtle.up(params[0])
                    return 0
                elif nom_procediment == "down":
                    self.turtle.down(params[0])
                    return 0
                elif nom_procediment == "show":
                    self.turtle.show()
                    return 0
                elif nom_procediment == "hide":
                    self.turtle.hide()
                    return 0
                elif nom_procediment == "color":
                    self.turtle.color(params[0], params[1], params[2])
                    return 0
                elif nom_procediment == "home":
                    self.turtle.home()
                    return 0
                else:
                    raise NameError("Procediment " +
                                    nom_procediment + " no declarat.")
        else:  # len(l) == 3 -> es tracta d'una expressio de SUM, RES, MUL, POW, DIV o NUM.NUM
            operator = l[1].getText()
            if operator == '+':
                return float(self.visit(l[0]) + self.visit(l[2]))
            elif operator == '-':
                return float(self.visit(l[0]) - self.visit(l[2]))
            elif operator == '*':
                return float(self.visit(l[0]) * self.visit(l[2]))
            elif operator == '**':
                return float(self.visit(l[0]) ** self.visit(l[2]))
            elif operator == '/':
                return float(self.visit(l[0]) / self.visit(l[2]))
            else:  # es de la forma num.num
                return float(l[0].getText() + '.' + l[2].getText())

    # Condicio

    def visitCond(self, ctx):
        l = list(ctx.getChildren())
        a = float(self.visit(l[0]))
        b = float(self.visit(l[2]))
        if l[1].getText() == '<':
            return a < b
        elif l[1].getText() == '<=':
            return a <= b
        elif l[1].getText() == '==':
            return a == b
        elif l[1].getText() == '!=':
            return a != b
        elif l[1].getText() == '>=':
            return a >= b
        else:
            return a > b
