from .utils import Clause, Variable
import itertools as it

class Generator:
    def __init__(self):
        pass
    
    def createDict(self):
        data = {}
        for x in range(1,10):
            for y in range(1,10):
                for val in range(1,10):
                    name = str.format("x {} {} {}",x,y,val)
                    data[name] = {"value": Variable(name), "clause": []}
                    data["!"+name] = {"value": Variable("!"+name,True), "clause": []}
        return data

    def createClause(self, data:dict, listVar:list, listVarNot:list, listC:list):
        clause = Clause(listVar)
        listC.append(clause)
        for var in listVar:
            data[var.name]['clause'].append(clause)
        for listClause in it.combinations(listVarNot,2):
            clause = Clause(list(listClause))
            listC.append(clause)
            for var in listClause:
                data[var.name]['clause'].append(clause)
    
    def genClause(self, data:dict, listClause:list):
        for x in range(1,10):
            for y in range(1,10):
                self.eachCell(x,y,data,listClause)
        for x in range(1,10):
            for val in range(1,10):
                self.eachRow(x,val,data,listClause)
        for y in range(1,10):
            for val in range(1,10):
                self.eachColumn(y,val,data,listClause)
        for xSquare in range(1,10,3):
            for ySquare in range(1,10,3):
                for val in range(1,10):
                    self.eachSquare(xSquare,ySquare,val,data,listClause)
    
    # Dans chaque case, il y a un chiffre et un seul
    def eachCell(self, x:int, y:int, data:dict, list:list):
        listVar = []
        listVarNot = []
        for val in range(1,10):
            listVar.append(data[str.format("x {} {} {}",x,y,val)]['value'])
            listVarNot.append(data[str.format("!x {} {} {}",x,y,val)]['value'])
        self.createClause(data,listVar,listVarNot,list)

    # Dans chaque ligne, chaque chiffre doit apparaître 1 fois et une seule
    def eachRow(self, x:int, val:int, data:dict, list:list):
        listVar = []
        listVarNot = []
        for y in range(1,10):
            listVar.append(data[str.format("x {} {} {}",x,y,val)]['value'])
            listVarNot.append(data[str.format("!x {} {} {}",x,y,val)]['value'])
        self.createClause(data,listVar,listVarNot,list)

    # Dans chaque colonne, chaque chiffre doit apparaître 1 fois et une seule
    def eachColumn(self, y:int, val:int, data:dict, list:list):
        listVar = []
        listVarNot = []
        for x in range(1,10):
            listVar.append(data[str.format("x {} {} {}",x,y,val)]['value'])
            listVarNot.append(data[str.format("!x {} {} {}",x,y,val)]['value'])
        self.createClause(data,listVar,listVarNot,list)

    # Dans chaque carré, chaque chiffre doit apparaître 1 fois et une seule
    def eachSquare(self, xSquare:int, ySquare:int, val:int, data:dict, list:list):
        listVar = []
        listVarNot = []
        for x in range(xSquare,xSquare+3):
            for y in range(ySquare,ySquare+3):
                listVar.append(data[str.format("x {} {} {}",x,y,val)]['value'])
                listVarNot.append(data[str.format("!x {} {} {}",x,y,val)]['value'])
        self.createClause(data,listVar,listVarNot,list)
    
    def createNumberClause(self, list_litt:list, data:dict, listClause:list):
        for l in list_litt:
            clause = Clause([data[l]["value"]])
            data[l]["clause"].append(clause)
            listClause.append(clause)