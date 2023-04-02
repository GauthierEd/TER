# https://www2.cs.sfu.ca/CourseCentral/827/havens/papers/topic%237(NoGoodLearning)/Clause%20Watching/ws-sat02-b.pdf

class Clause:
    def __init__(self, list_litteraux):
        # La liste contient les identifiants des variables du dictionnaire
        self.list_litteraux = list_litteraux
        self.nb_litt_satisfied = 0
        self.nb_litt_unsatisfied = len(list_litteraux)

    def isSatisfy(self):
        if self.nb_litt_satisfied >= 1:
            return True
        elif self.nb_litt_unsatisfied == len(self.list_litteraux):
            return False
        else:
            return False

    def isUnit(self):
        if self.nb_litt_satisfied == 0 and self.nb_litt_unsatisfied ==  1:
            return True
        else:
            return False
        
    def isNotValid(self):
        if self.nb_litt_satisfied == 0 and self.nb_litt_unsatisfied == 0:
            return True
        else:
            return False

    def __repr__(self):
        txt = ""
        for l in self.list_litteraux:
            txt += " " + l.name
        return(f'{txt}, {self.nb_litt_satisfied}, {self.nb_litt_unsatisfied}')


# Objet qui represente une variable, contient sa valeur et s'il est une négation ou pas
class Variable:
    def __init__(self, name, isNot = False):
        # Nom de la variable
        self.name = name
        # Valeur de la variable, None si pas initialisé, 1 pour vrai, -1 pour faux
        self.value = None
        self.nb_clause_in = 0

    def __repr__(self) -> str:
        #return(f'Nom: {self.name}, Valeur: {self.value}, isNot: {self.isNot}')
        return(f'{self.name}, {self.nb_clause_in}, {self.value}')

    def setValue(self, value):
        self.value = value