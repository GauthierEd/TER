from .utils import Clause, Variable
import itertools as it

class Dames:
    def __init__(self, size:int):
        self.size = size

    def createDict(self):
        data = {}
        for x in range(1,self.size+1):
            for y in range(1,self.size+1):
                name = str.format("x {} {}",x,y)
                data[name] = {"value": Variable(name), "clause": []}
                data["!"+name] = {"value": Variable("!"+name,True), "clause": []}
        return data
    
    def genClause(self, data:dict, listClause:list):
        for x in range(1,self.size+1):
            self.eachRow(x,data,listClause)
        for y in range(1,self.size+1):
            self.eachColumn(y,data,listClause)
        for i in range(1,self.size):
            self.eachDiag1(i,data,listClause)
        for i in range(self.size,1,-1):
            self.eachDiag2(i,data,listClause)
        for key, value in data.items():
            value["value"].nb_clause_in = len(value["clause"])

    def eachRow(self, x:int, data:dict, listClause:list):
        listVar = []
        listVarNot = []
        for y in range(1,self.size+1):
            listVar.append(data[str.format("x {} {}",y,x)]['value'])
            listVarNot.append(data[str.format("!x {} {}",y,x)]['value'])
        self.createClause(data,listVar,listVarNot,listClause)

    def eachColumn(self, y:int, data:dict, listClause:list):
        listVarNot = []
        for x in range(1,self.size+1):
            listVarNot.append(data[str.format("!x {} {}",y,x)]['value'])
        self.createClause(data,[],listVarNot,listClause, True)

    def eachDiag1(self, i:int, data:dict, listClause:list):
        listVarNot1 = []
        listVarNot2 = []
        k = 1
        for j in range(i, self.size+1):
            listVarNot1.append(data[str.format("!x {} {}",j,k)]["value"])
            listVarNot2.append(data[str.format("!x {} {}",k,j)]["value"])
            k += 1
        self.createClause(data, [], listVarNot1, listClause, True)
        self.createClause(data, [], listVarNot2, listClause, True)

    def eachDiag2(self, i:int, data:dict, listClause:list):
        listVarNot1 = []
        listVarNot2 = []
        k = 1
        for j in range(i, 0, -1):
            listVarNot1.append(data[str.format("!x {} {}",j,k)]["value"])
            k += 1
        k = self.size+1-i
        for j in range(self.size, self.size-i, -1):
            listVarNot2.append(data[str.format("!x {} {}",k,j)]["value"])
            k += 1
        self.createClause(data, [], listVarNot1, listClause, True)
        self.createClause(data, [], listVarNot2, listClause, True)

    def createClause(self, data:dict, listVar:list, listVarNot:list, listClause:list, noMinOne:bool=False):
        if not noMinOne:
            clause = Clause(listVar)
            listClause.append(clause)
            for var in listVar:
                data[var.name]['clause'].append(clause)
        for listC in it.combinations(listVarNot,2):
            clause = Clause(list(listC))
            listClause.append(clause)
            for var in listC:
                data[var.name]['clause'].append(clause)