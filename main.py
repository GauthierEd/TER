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
    
def CreateDict():
    data = {}
    for x in range(1,10):
        for y in range(1,10):
            for val in range(1,10):
                data[str.format("x {} {} {}",x,y,val)] = {"value": Variable(), "clause": []}
                data[str.format("!x {} {} {}",x,y,val)] = {"value": Variable(True), "clause": []}
    return data

def GenClause(data:dict):
    clauseList = []
    eachCell(data)
    eachRow(data)
    eachColumn(data)
    eachSquare(data)
    return clauseList

def eachCell(data:dict):
    for i in range(1,10):
        for j in range(1,10):
            listVarClause = []
            for key, value in data.items():
                s = str.split(key)
                if s[1] == str(i) and s[2] == str(j):
                    listVarClause.append(value.value)


def eachRow(data:dict):
    pass

def eachColumn(data:dict):
    pass

def eachSquare(data:dict):
    pass

data = CreateDict()
GenClause(data)