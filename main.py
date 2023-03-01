# https://www2.cs.sfu.ca/CourseCentral/827/havens/papers/topic%237(NoGoodLearning)/Clause%20Watching/ws-sat02-b.pdf

# Objet qui represente une clause, contient la liste des variables de la clauses
class Clause:
    def __init__(self, list_litteraux):
        # La liste contient les identifiants des variables du dictionnaire
        self.list_litteraux = list_litteraux
        # Une clause est satisfaite si nb_litteraux_satis > 0
        self.nb_litteraux_satis = 0
        # Une clause est insatisfaite si nb_litteraux_nsatis == nb_littéraux de la clause
        self.nb_literraux_nsatis = 0
    
    def isSatisfy(self):
        pass

# Objet qui represente une variable, contient sa valeur et s'il est une négation ou pas
class Variable:
    def __init__(self, isNot = False):
        # Valeur de la variable, None si pas initialisé, 1 pour vrai, -1 pour faux
        self.value = None
        # Booleen pour savoir si variable est x111 ou !x111 pour calculer sa valeur
        self.isNot = isNot
    
    def __repr__(self) -> str:
        return(f'Valeur: {self.getValue()}, isNot: {self.isNot}')

    def setValue(self, value):
        self.value = value
    
    def getValue(self):
        if not self.isNot:
            return self.value
        else:
            return not self.value
    

data = {
    # Pour la variable à la ligne 1, colonne 1 pour le chiffre 1
    "x111": {
        "value": Variable(),
        # Liste de toutes les clauses dans laquel la variable est présente
        "clause": []
    },
    # Pour la négation de la variable à la ligne 1, colonne 1 pour le chiffre 1
    "!x111": {
        "value": Variable(True),
        "clause": []
    },
    "x112": {
        "value": Variable(),
        "clause": []
    },
    "!x112": {
        "value": Variable(True),
        "clause": []
    }
}
