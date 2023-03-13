# https://www2.cs.sfu.ca/CourseCentral/827/havens/papers/topic%237(NoGoodLearning)/Clause%20Watching/ws-sat02-b.pdf
import itertools as it

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
    
def CreateDict():
    data = {}
    for x in range(1,10):
        for y in range(1,10):
            for val in range(1,10):
                name = str.format("x {} {} {}",x,y,val)
                data[name] = {"value": Variable(name), "clause": []}
                data["!"+name] = {"value": Variable("!"+name,True), "clause": []}
    return data

def GenClause(data:dict,listClause:list):
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
    clause = Clause(listVar)
    list.append(clause)
    for var in listVar:
        data[var.name]['clause'].append(clause)
    for listClause in it.combinations(listVarNot,2):
        list.append(Clause(listClause))
        for var in listClause:
            data[var.name]['clause'].append(clause)

# Dans chaque ligne, chaque chiffre doit apparaître 1 fois et une seule
def eachRow(x:int,val:int,data:dict,list:list):
    listVar = []
    listVarNot = []
    for y in range(1,10):
        listVar.append(data[str.format("x {} {} {}",x,y,val)]['value'])
        listVarNot.append(data[str.format("!x {} {} {}",x,y,val)]['value'])
    clause = Clause(listVar)
    list.append(clause)
    for var in listVar:
        data[var.name]['clause'].append(clause)
    for listClause in it.combinations(listVarNot,2):
        list.append(Clause(listClause))
        for var in listClause:
            data[var.name]['clause'].append(clause)

# Dans chaque colonne, chaque chiffre doit apparaître 1 fois et une seule
def eachColumn(y:int,val:int,data:dict,list:list):
    listVar = []
    listVarNot = []
    for x in range(1,10):
        listVar.append(data[str.format("x {} {} {}",x,y,val)]['value'])
        listVarNot.append(data[str.format("!x {} {} {}",x,y,val)]['value'])
    clause = Clause(listVar)
    list.append(clause)
    for var in listVar:
        data[var.name]['clause'].append(clause)
    for listClause in it.combinations(listVarNot,2):
        list.append(Clause(listClause))
        for var in listClause:
            data[var.name]['clause'].append(clause)

# Dans chaque carré, chaque chiffre doit apparaître 1 fois et une seule
def eachSquare(xSquare:int,ySquare:int,val:int,data:dict,list:list):
    listVar = []
    listVarNot = []
    for x in range(xSquare,xSquare+3):
        for y in range(ySquare,ySquare+3):
            listVar.append(data[str.format("x {} {} {}",x,y,val)]['value'])
            listVarNot.append(data[str.format("!x {} {} {}",x,y,val)]['value'])
    clause = Clause(listVar)
    list.append(clause)
    for var in listVar:
        data[var.name]['clause'].append(clause)
    for listClause in it.combinations(listVarNot,2):
        list.append(Clause(listClause))
        for var in listClause:
            data[var.name]['clause'].append(clause)

data = CreateDict()
listClause = []
GenClause(data,listClause)
print("Le nombre de variable propositionnelles est de {} et le nombre de clause est de {}".format(int(data.__len__()/2),listClause.__len__()))