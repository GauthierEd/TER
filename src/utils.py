# https://www2.cs.sfu.ca/CourseCentral/827/havens/papers/topic%237(NoGoodLearning)/Clause%20Watching/ws-sat02-b.pdf

class Clause:
    def __init__(self, list_litteraux):
        # La liste contient les identifiants des variables du dictionnaire
        self.list_litteraux:list = list_litteraux

    def __repr__(self):
        txt = ""
        for l in self.list_litteraux:
            txt += " " + l.name
        return txt


# Objet qui represente une variable, contient sa valeur et s'il est une négation ou pas
class Variable:
    def __init__(self, name, isNot = False):
        # Nom de la variable
        self.name = name
        # Valeur de la variable, None si pas initialisé, 1 pour vrai, -1 pour faux
        self.value = None
        # Booleen pour savoir si variable est x111 ou !x111 pour calculer sa valeur
        self.isNot = isNot
    
    def __repr__(self) -> str:
        return(f'Nom: {self.name}, Valeur: {self.value}, isNot: {self.isNot}')


    def setValue(self, value):
        self.value = value
    
    def getValue(self):
        if not self.isNot or self.value == None:
            return self.value
        else :
            return not self.value