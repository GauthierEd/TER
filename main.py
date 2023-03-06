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

    def __repr__(self) -> str:
        return("^".join(self.list_litteraux))
    
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
        if not self.isNot or self.value == None:
            return self.value
        else:
            return not self.value
    
def dpll(data, litteral = None):
    print("litteral", litteral)
    clause_empty = []
    clause_uni = set()
    if litteral != None:
        clause_uni.add(Clause([litteral]))
    # Propagation unitaire
    # Recherche de toutes les clauses unitaires
    for key, value in data.items():
        for clause in value["clause"]:
            if len(clause.list_litteraux) == 1:
                clause_uni.add(clause)
    for clause in clause_uni:
        litt = clause.list_litteraux[0]
        if "!" in litt:
            # Met !x à faux
            data[litt]["value"].setValue(False)
            # Supprime toutes les clauses où !x apparait car elles sont satisfaites
            for clause in list(data[litt]["clause"]):
                clause_litt = clause.list_litteraux
                for l in clause_litt:
                    data[l]["clause"].remove(clause)
                    
            # Supprime x dans toutes les clauses où il apparait
            inv_litt = litt.split("!")[1]
            data[inv_litt]["value"].setValue(False)
            for clause in list(data[inv_litt]["clause"]):
                # On supprimer aussi x des autres clauses car ils sont passé en copy dans le dict
                """for l in list(clause.list_litteraux):
                    for clause_l in data[l]["clause"]:
                        if l in clause_l.list_litteraux:
                            clause_l.list_litteraux.remove(l)"""
                clause.list_litteraux.remove(inv_litt)
                # Si la clause est vide, on la garde en mémoire
                if len(clause.list_litteraux) == 0:
                    clause_empty.append(clause)
            data[inv_litt]["clause"] = []
           
        else:
            # Met x à vrai
            data[litt]["value"].setValue(True)
            # Supprime toutes les clauses où x apparait car elles sont satisfaites
            for clause in list(data[litt]["clause"]):
                clause_litt = clause.list_litteraux
                for l in clause_litt:
                    data[l]["clause"].remove(clause)
            # Supprime !x dans toutes les clauses où il apparait
            inv_litt = "!" + litt
            data[inv_litt]["value"].setValue(True)
            for clause in list(data[inv_litt]["clause"]):
                # On supprimer aussi x des autres clauses car ils sont passé en copy dans le dict
                """for l in list(clause.list_litteraux):
                    for clause_l in data[l]["clause"]:
                        if l in clause_l.list_litteraux:
                            clause_l.list_litteraux.remove(l)"""
                clause.list_litteraux.remove(inv_litt)
                # Si la clause est vide, on la garde en mémoire
                if len(clause.list_litteraux) == 0:
                    clause_empty.append(clause)
            data[inv_litt]["clause"] = []

    #### LITTERAUX PURE ####
    all_values = list(test.values())
    for i in range(0,len(all_values), 2):
        x_values = all_values[i]
        notX_values = all_values[i+1]
        if len(x_values["clause"]) == 0 and len(notX_values["clause"]) > 0:
            notX_values["value"].setValue(False)
            # Supprime toutes les clauses où !x apparait car elles sont satisfaites
            for clause in list(notX_values["clause"]):
                clause_litt = clause.list_litteraux
                for l in clause_litt:
                    data[l]["clause"].remove(clause)
        elif len(x_values["clause"]) > 0 and len(notX_values["clause"]) == 0:
            x_values["value"].setValue(True)
            # Supprime toutes les clauses où x apparait car elles sont satisfaites
            for clause in list(x_values["clause"]):
                clause_litt = clause.list_litteraux
                for l in clause_litt:
                    data[l]["clause"].remove(clause)

    # Test si il y a plus de clause
    isEmpty = True
    for key, value in data.items():
        if len(value["clause"]) > 0:
            isEmpty = False
    if isEmpty:
        return data
    
    # Test s'il existe des clauses vides
    if len(clause_empty) > 0:
        return False
            
    # On choisit un litteral, on prends le 1er litteral qui n'a pas encore de valeur associé
    for key, value in data.items():
        if value["value"].getValue() == None and len(value["clause"]) > 0:
            new_litteral = key
            break
    
    result = dpll(deepcopy(data), new_litteral)
    if result:
        return result
    result = dpll(deepcopy(data), "!"+new_litteral)
    if result:
        return result
    else:
        return False

#### ENSEMBLE DE CLAUSE DE TEST #####
c1 = Clause(["x 1", "x 2", "!x 3"])
c2 = Clause(["!x 1", "x 2", "x 3"])
c3 = Clause(["!x 2"])
c4 = Clause(["x 2", "x 3"])
c5 = Clause(["x 1", "!x 2"])
test = {
    "x 1":{
        "value": Variable(),
        "clause": [c1, c5]
    },
    "!x 1":{
        "value": Variable(True),
        "clause": [c2]
    },
    "x 2":{
        "value": Variable(),
        "clause": [c1, c2, c4]
    },
    "!x 2":{
        "value": Variable(True),
        "clause": [c3, c5]
    },
    "x 3":{
        "value": Variable(),
        "clause": [c2, c4]
    },
    "!x 3":{
        "value": Variable(True),
        "clause": [c1]
    }
}


result_dpll = dpll(test)
if not result_dpll:
    print("Pas de modele")
else:
    print(result_dpll)
