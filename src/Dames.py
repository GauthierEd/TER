from .utils import Clause, Variable
import itertools as it

class Dames:
    def __init__(self):
        pass

    def createDict(self):
        data = {}
        for x in range(1,9):
            for y in range(1,9):
                name = str.format("x {} {}",x,y)
                data[name] = {"value": Variable(name), "clause": []}
                data["!"+name] = {"value": Variable("!"+name,True), "clause": []}
        return data
    
    def genClause(self, data:dict, listClause:list):
        for x in range(1,9):
            self.eachRow(x,data,listClause)
        for y in range(1,9):
            self.eachColumn(y,data,listClause)
        for x in range(1,9):
            for y in range(1,9):
                self.eachDiag(x,y,data,listClause)
            
    def eachRow(self, x:int, data:dict, list:list):
        listVar = []
        listVarNot = []
        for y in range(1,9):
            listVar.append(data[str.format("x {} {}",x,y)]['value'])
            listVarNot.append(data[str.format("!x {} {}",x,y)]['value'])
        self.createClause(data,listVar,listVarNot,list)

    def eachColumn(self, y:int, data:dict, list:list):
        listVar = []
        listVarNot = []
        for x in range(1,9):
            listVar.append(data[str.format("x {} {}",x,y)]['value'])
            listVarNot.append(data[str.format("!x {} {}",x,y)]['value'])
        self.createClause(data,listVar,listVarNot,list)

    def eachDiag(self, x:int, y:int, data:dict, listC:list):
        listVar = []
        listVarNot = []
        #Diagonale Haut Gauche
        self.calculDiag(x,y,data,listVar,listVarNot,False,False)
        #Diagonale Bas Droite
        self.calculDiag(x,y,data,listVar,listVarNot,True,True)
        #Diagonale Bas Gauche
        self.calculDiag(x,y,data,listVar,listVarNot,False,True)
        #Diagonale Haut Droite
        self.calculDiag(x,y,data,listVar,listVarNot,True,False)
        listVar = list(set(listVar))
        listVarNot = list(set(listVarNot))
        self.createClause(data,listVar,listVarNot,listC)

    def calculDiag(self, x:int, y:int, data:dict, listVar:list,listVarNot:list,xPlus:bool,yPlus:bool):
        xtemp = x
        ytemp = y
        if xPlus:
            xLimit = 9
        else:
            xLimit = 0
        if yPlus:
            yLimit = 9
        else:
            yLimit = 0
        while xtemp != xLimit and ytemp != yLimit:
            listVar.append(data[str.format("x {} {}",xtemp,ytemp)]['value'])
            listVarNot.append(data[str.format("!x {} {}",xtemp,ytemp)]['value'])
            if xPlus:
                xtemp += 1
            else:
                xtemp -= 1
            if yPlus:
                ytemp += 1
            else:
                ytemp -= 1

    def createClause(self, data:dict, listVar:list, listVarNot:list, list:list):
        clause = Clause(listVar)
        list.append(clause)
        for var in listVar:
            data[var.name]['clause'].append(clause)
        for listClause in it.combinations(listVarNot,2):
            clause = Clause(listClause)
            list.append(clause)
            for var in listClause:
                data[var.name]['clause'].append(clause)
    
dames = Dames()
d = dames.createDict()
l = []
dames.genClause(d,l)
l