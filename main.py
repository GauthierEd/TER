# https://www2.cs.sfu.ca/CourseCentral/827/havens/papers/topic%237(NoGoodLearning)/Clause%20Watching/ws-sat02-b.pdf

# Objet qui represente une clause, contient la liste des variables de la clauses
from copy import deepcopy


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
    
def dpll(data, litteral = None):
    # litteral sous la forme : "x 1 1 1" ou "!x 1 1 1"
    clause_empty = []
    clause_uni = set()
    if litteral != None:
        clause_uni.add(Clause([litteral]))
    # Propagation unitaire
    # Recherche de toutes les clauses unitaires
    for key in data:
        for clause in data[key].clause:
            if len(clause.list_litteraux) == 1:
                clause_uni.add(clause)
    for clause in clause_uni:
        litt = clause.list_litteraux[0]
        if "!" in litt:
            # Met !x à faux
            data[litt].value.setValue(False)
            # Supprime toutes les clauses où !x apparait car elles sont satisfaites
            for clause in data[litt].clause:
                clause_litt = clause.list_litteraux
                for l in clause_litt:
                    data[l].clause.remove(clause)
            # Supprime x dans toutes les clauses où il apparait
            inv_litt = litt.split("!")[1]
            for clause in data[inv_litt].clause:
                clause.list_litteraux.remove(inv_litt)
                # Si la clause est vide, on la garde en mémoire
                if len(clause.list_litteraux) == 0:
                    clause_empty.append(clause)
        else:
            # Met x à vrai
            data[litt].value.setValue(True)
            # Supprime toutes les clauses où x apparait car elles sont satisfaites
            for clause in data[litt].clause:
                clause_litt = clause.list_litteraux
                for l in clause_litt:
                    data[l].clause.remove(clause)
            # Supprime !x dans toutes les clauses où il apparait
            inv_litt = "!" + litt
            for clause in data[inv_litt].clause:
                clause.list_litteraux.remove(inv_litt)
                # Si la clause est vide, on la garde en mémoire
                if len(clause.list_litteraux) == 0:
                    clause_empty.append(clause)

    # Test si il y a plus de clause
    isEmpty = True
    for key in data:
        if len(data[key].clause) > 0:
            isEmpty = False
    if isEmpty:
        return data
    
    # Test s'il existe des clauses vides
    if len(clause_empty) > 0:
        return False
            
    # On choisit un litteral, on prends le 1er litteral qui n'a pas encore de valeur associé
    for key in data:
        if data[key].value.getValue() == None and len(data[key].clause) > 0:
            new_litteral = key
    
    result = dpll(deepcopy(data), new_litteral)
    if result:
        return result
    result = dpll(deepcopy(data), "!"+new_litteral)
    if result:
        return result
    else:
        return False
    
