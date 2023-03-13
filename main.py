# https://www2.cs.sfu.ca/CourseCentral/827/havens/papers/topic%237(NoGoodLearning)/Clause%20Watching/ws-sat02-b.pdf

# Objet qui represente une clause, contient la liste des variables de la clauses
from copy import deepcopy
import itertools as it
import numpy as np

class Clause:
    def __init__(self, list_litteraux):
        # La liste contient les identifiants des variables du dictionnaire
        self.list_litteraux:list = list_litteraux
        # Une clause est satisfaite si nb_litteraux_satis > 0
        self.nb_litteraux_satis = 0
        # Une clause est insatisfaite si nb_litteraux_nsatis == nb_littéraux de la clause
        self.nb_literraux_nsatis = 0

    #def __repr__(self) -> str:
        #return("^".join(self.list_litteraux))
    
    def isSatisfy(self):
        pass

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
        return(f'Nom: {self.name}, Valeur: {self.getValue()}, isNot: {self.isNot}')

    def setValue(self, value):
        self.value = value
    
    def getValue(self):
        if not self.isNot or self.value == None:
            return self.value
        else :
            return not self.value

def createDict():
    data = {}
    for x in range(1,10):
        for y in range(1,10):
            for val in range(1,10):
                name = str.format("x {} {} {}",x,y,val)
                data[name] = {"value": Variable(name), "clause": []}
                data["!"+name] = {"value": Variable("!"+name,True), "clause": []}
    return data

def genClause(data:dict,listClause:list):
    for x in range(1,10):
        for y in range(1,10):
            eachCell(x,y,data,listClause)
    for x in range(1,10):
        for val in range(1,10):
            eachRow(x,val,data,listClause)
    for y in range(1,10):
        for val in range(1,10):
            eachColumn(y,val,data,listClause)
    for xSquare in range(1,10,3):
        for ySquare in range(1,10,3):
            for val in range(1,10):
                eachSquare(xSquare,ySquare,val,data,listClause)

# Dans chaque case, il y a un chiffre et un seul
def eachCell(x:int,y:int,data:dict,list:list):
    listVar = []
    listVarNot = []
    for val in range(1,10):
        listVar.append(data[str.format("x {} {} {}",x,y,val)]['value'])
        listVarNot.append(data[str.format("!x {} {} {}",x,y,val)]['value'])
    createClause(data,listVar,listVarNot,list)

# Dans chaque ligne, chaque chiffre doit apparaître 1 fois et une seule
def eachRow(x:int,val:int,data:dict,list:list):
    listVar = []
    listVarNot = []
    for y in range(1,10):
        listVar.append(data[str.format("x {} {} {}",x,y,val)]['value'])
        listVarNot.append(data[str.format("!x {} {} {}",x,y,val)]['value'])
    createClause(data,listVar,listVarNot,list)

# Dans chaque colonne, chaque chiffre doit apparaître 1 fois et une seule
def eachColumn(y:int,val:int,data:dict,list:list):
    listVar = []
    listVarNot = []
    for x in range(1,10):
        listVar.append(data[str.format("x {} {} {}",x,y,val)]['value'])
        listVarNot.append(data[str.format("!x {} {} {}",x,y,val)]['value'])
    createClause(data,listVar,listVarNot,list)

# Dans chaque carré, chaque chiffre doit apparaître 1 fois et une seule
def eachSquare(xSquare:int,ySquare:int,val:int,data:dict,list:list):
    listVar = []
    listVarNot = []
    for x in range(xSquare,xSquare+3):
        for y in range(ySquare,ySquare+3):
            listVar.append(data[str.format("x {} {} {}",x,y,val)]['value'])
            listVarNot.append(data[str.format("!x {} {} {}",x,y,val)]['value'])
    createClause(data,listVar,listVarNot,list)

def createClause(data:dict,listVar:list,listVarNot:list,list:list):
    clause = Clause(listVar)
    list.append(clause)
    for var in listVar:
        data[var.name]['clause'].append(clause)
    for listClause in it.combinations(listVarNot,2):
        clause = Clause(listClause)
        list.append(clause)
        for var in listClause:
            data[var.name]['clause'].append(clause)


def dpll(data, litteral = None):
    clause_empty = []
    clause_uni = set()
    if litteral != None:
        clause_uni.add(Clause([data[litteral]["value"]]))
    # Propagation unitaire
    # Recherche de toutes les clauses unitaires
    for key, value in data.items():
        for clause in value["clause"]:
            if len(clause.list_litteraux) == 1:
                clause_uni.add(clause)
    for clause in clause_uni:
        if len(clause.list_litteraux) > 0:
            litt = clause.list_litteraux[0].name
        if "!" in litt:
            # Met !x à faux
            data[litt]["value"].setValue(False)
            # Supprime toutes les clauses où !x apparait car elles sont satisfaites
            for clause in data[litt]["clause"]:
                clause_litt = clause.list_litteraux
                for l in clause_litt:
                    data[l.name]["clause"].remove(clause)
                    
            # Supprime x dans toutes les clauses où il apparait
            inv_litt = litt.split("!")[1]
            data[inv_litt]["value"].setValue(False)
            for clause in data[inv_litt]["clause"]:
                # On supprimer aussi x des autres clauses car ils sont passé en copy dans le dict
                clause.list_litteraux = list(clause.list_litteraux)
                clause.list_litteraux.remove(data[inv_litt]["value"])
                # Si la clause est vide, on la garde en mémoire
                if len(clause.list_litteraux) == 0:
                    clause_empty.append(clause)
            data[inv_litt]["clause"] = []
           
        else:
            # Met x à vrai
            data[litt]["value"].setValue(True)
            # Supprime toutes les clauses où x apparait car elles sont satisfaites
            for clause in data[litt]["clause"]:
                clause_litt = clause.list_litteraux
                for l in clause_litt:
                    data[l.name]["clause"].remove(clause)
            # Supprime !x dans toutes les clauses où il apparait
            inv_litt = "!" + litt
            data[inv_litt]["value"].setValue(True)
            for clause in data[inv_litt]["clause"]:
                # On supprimer aussi x des autres clauses car ils sont passé en copy dans le dict
                clause.list_litteraux = list(clause.list_litteraux)
                clause.list_litteraux.remove(data[inv_litt]["value"])
                # Si la clause est vide, on la garde en mémoire
                if len(clause.list_litteraux) == 0:
                    clause_empty.append(clause)
            data[inv_litt]["clause"] = []

    #### LITTERAUX PURE ####
    all_values = list(data.values())
    for i in range(0,len(all_values), 2):
        x_values = all_values[i]
        notX_values = all_values[i+1]
        if len(x_values["clause"]) == 0 and len(notX_values["clause"]) > 0:
            notX_values["value"].setValue(False)
            # Supprime toutes les clauses où !x apparait car elles sont satisfaites
            for clause in list(notX_values["clause"]):
                clause_litt = clause.list_litteraux
                for l in clause_litt:
                    if len(data[l.name]["clause"]) > 0:
                        data[l.name]["clause"].remove(clause)
        elif len(x_values["clause"]) > 0 and len(notX_values["clause"]) == 0:
            x_values["value"].setValue(True)
            # Supprime toutes les clauses où x apparait car elles sont satisfaites
            for clause in list(x_values["clause"]):
                clause_litt = clause.list_litteraux
                for l in clause_litt:
                    if len(data[l.name]["clause"]) > 0:
                        data[l.name]["clause"].remove(clause)

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


data = createDict()
listClause = []
genClause(data,listClause)
print("Le nombre de variable propositionnelles est de {} et le nombre de clause est de {}".format(int(data.__len__()/2),listClause.__len__()))
litt = ["x 1 1 8", "x 8 1 7", "x 3 2 6", "x 5 2 1", "x 8 2 5", "x 9 2 3", "x 2 3 4", "x 4 3 6", "x 5 4 8", "x 7 4 4", "x 3 5 3", "x 7 5 7", 
                          "x 2 6 2", "x 6 6 5", "x 8 6 3","x 9 6 8", "x 7 7 8", "x 3 8 4", "x 5 8 5", "x 8 8 6", "x 9 8 1", "x 1 9 9", "x 6 9 2"]
for l in litt:
    clause = Clause([data[l]["value"]])
    data[l]["clause"].append(clause)
    listClause.append(clause)



result_dpll = dpll(data)
if not result_dpll:
    print("Pas de modele")
else:
    print("Un modele")

m = np.zeros((9,9))
for i in range(1,10):
    for j in range(1,10):
        for k in range(1,10):
            if result_dpll[str.format("x {} {} {}",i,j,k)]["value"].value:
                m[j-1][i-1] = k
                break
print(m)