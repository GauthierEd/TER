from copy import deepcopy
from .utils import Clause
import random
import numpy as np

#https://www.cs.cmu.edu/~15414/s20/2018/lectures/20-sat-techniques.pdf
#https://baldur.iti.kit.edu/sat/files/2018/l05.pdf

class Solver:
    def __init__(self, heuristic = 1):
        self.heuristic = heuristic
        self.all_solution = []
        self.get_all_solution = False
        self.recursivity = 0
        self.branch_close = 0
        self.nb_clause = 0
        self.nb_clause_satisfy = 0
        self.backtracking = []
        self.indexBacktracking = -1
        self.moms_data = None
        self.size_max = 0

    def set_all_solution(self, choice):
        self.get_all_solution = choice
        if self.get_all_solution:
            print("Cherche toutes les solutions")
        else:
            print("Cherche une solution")

    def set_heuristic(self,choice):
        self.heuristic = choice
        print("Utilise heuristic", choice)
    
    def S(self, clause, litteral):
        k = 2
        if "!" in litteral:
            litteral = litteral.split("!")[1]  
        return (self.f(clause,litteral) + self.f(clause,'!'+litteral)) * pow(2,k) + (self.f(clause,litteral) * self.f(clause,"!"+litteral))

    
    def f(self, clause, litteral):
        # Renvoie le nombre d'occurence d'un litteral dans toutes les plus petites
        # clauses non satisfaites et non unitaire
        occur = 0
        for litt in clause.list_litteraux:
            if litt.name == litteral:
                occur += 1
        return occur
    
    def h(self, data, i, litteral):
        count = 0
        for clause in data[litteral]["clause"]:
            if len(clause.list_litteraux) == i and clause.nb_litt_satisfied == 0:
                count += 1
        return count

    def H(self, data, i, litteral):
        alpha = 1
        beta = 2
        return alpha * max(self.h(data,i,litteral), self.h(data,i,'!'+litteral)) + beta * min(self.h(data,i,litteral), self.h(data,i,'!'+litteral))

    def dpll(self, data, litteral = None, clause_unit = []):
        self.recursivity += 1
        clause_empty = [False]
        next_clause_unit = []
        litt_false = []
        litt_true = []
        self.indexBacktracking += 1
        if litteral != None:
            clause_unit.insert(0, Clause([data[litteral]["value"]]))
        #### PROPAGATION UNITAIRE ####
        for clause in clause_unit:
            if clause_empty[0]:
                break
            litt = None
            for l in clause.list_litteraux:
                if l.value == None:
                    litt = l.name
                    break
            if litt != None:
                self.unit_propagate(data, litt, clause_empty, next_clause_unit, litt_false, litt_true)
        clause_unit = next_clause_unit
        #### LITTERAUX PURE ####
        if not clause_empty[0]:
            self.pure_literal(data, litt_true, litt_false)

        self.backtracking.append({
            "litt_true": litt_true,
            "litt_false": litt_false
        })

        # Test s'il existe des clauses vides
        if clause_empty[0]:
            self.branch_close += 1
            return False
        
        # Test si il y a plus de clause
        isEmpty = False
        if self.nb_clause_satisfy == self.nb_clause:
            isEmpty = True
    
        if isEmpty and not self.get_all_solution:
            return data
        elif isEmpty and self.get_all_solution:
            self.all_solution.append(deepcopy(data))
            return True

        new_litteral = None
        if self.heuristic == 1:
            # On choisit un litteral, on prends le 1er litteral qui n'a pas encore de valeur associé
            for key, value in data.items():
                if value["value"].value == None and value["value"].nb_clause_in > 0:
                    new_litteral = key
                    break
        elif self.heuristic == 2:
            all_keys = []
            for key, value in data.items():
                if value["value"].value == None and value["value"].nb_clause_in > 0:
                    all_keys.append(key)
            new_litteral = random.choice(all_keys)
        elif self.heuristic == 3:
            # BOHM'S Heuristic
            keys = list(data.keys())
            maxVector = (0, 0)
            for i in range(0,len(keys), 2):
                key = keys[i]
                if data[key]["value"].value == None:
                    vector = (self.H(data, 2, key), self.H(data, self.size_max, key))
                    if vector > maxVector:
                        maxVector = vector
                        new_litteral = key
        elif self.heuristic == 4:
            # MOMS Heuristic
            # smallest_clause
            smallest_clause = None
            for clause in self.moms_data["2"]:
                if clause.nb_litt_satisfied == 0:
                    smallest_clause = clause
                    break
            if smallest_clause == None:
                for clause in self.moms_data[str(self.size_max)]:
                    if clause.nb_litt_satisfied == 0:
                        smallest_clause = clause
                        break
            maxOccur = 0
            for litteral in smallest_clause.list_litteraux:
                occur = self.S(smallest_clause,litteral.name)
                if occur > maxOccur:
                    maxOccur = occur
                    new_litteral = litteral.name
        elif self.heuristic == 5:
            #DLCS
            maxDLCS = 0
            keys = list(data.keys())
            for i in range(0,len(keys), 2):
                key = keys[i]
                notKey = keys[i+1]
                if data[key]["value"].value == None:
                    occurPos = 0
                    occurNeg = 0
                    for clause in data[key]["clause"]:
                        if clause.nb_litt_satisfied == 0:
                            occurPos += 1
                    for clause in data[notKey]["clause"]:
                        if clause.nb_litt_satisfied == 0:
                            occurNeg += 1
                    if (occurNeg + occurPos) > maxDLCS:
                        maxDLCS = (occurNeg + occurPos)
                        new_litteral = key
            pass
        elif self.heuristic == 6:
            #DLIS
            maxDLIS = 0
            keys = list(data.keys())
            for i in range(0,len(keys), 2):
                key = keys[i]
                notKey = keys[i+1]
                if data[key]["value"].value == None:
                    occurPos = 0
                    occurNeg = 0
                    for clause in data[key]["clause"]:
                        if clause.nb_litt_satisfied == 0:
                            occurPos += 1
                    for clause in data[notKey]["clause"]:
                        if clause.nb_litt_satisfied == 0:
                            occurNeg += 1
                    if max(occurPos, occurNeg) > maxDLIS:
                        maxDLIS = max(occurPos, occurNeg)
                        new_litteral = key
        
        if "!" in new_litteral:
            new_litteral = new_litteral.split("!")[1]  
        
        result = self.dpll(data = data, litteral = new_litteral, clause_unit = clause_unit)
        if litteral != None:
            clause_unit = clause_unit[1:]

        if result and not self.get_all_solution:
            return result
        
        if not result or (result and self.get_all_solution):
            self.make_backtracking(data)

        result = self.dpll(data = data, litteral = "!"+new_litteral, clause_unit = clause_unit)

        if not result or (result and self.get_all_solution):
            self.make_backtracking(data)
    
        if result and not self.get_all_solution:
            return result
        elif result and self.get_all_solution:
            return True
        else:
            return False

    def make_backtracking(self, data):
        for l in self.backtracking[self.indexBacktracking]["litt_true"]:
            data[l]["value"].setValue(None)
            if "!" in l:
                for clause in data[l]["clause"]:
                    clause.nb_litt_unsatisfied += 1
                    if not clause.isSatisfy():
                        data[l]["value"].nb_clause_in += 1
            else:
                for clause in data[l]["clause"]:
                    if clause.nb_litt_satisfied > 0:
                        clause.nb_litt_satisfied -= 1
                    if not clause.isSatisfy():
                        if self.nb_clause_satisfy > 0:
                            self.nb_clause_satisfy -= 1
                        for litt in clause.list_litteraux:
                            data[litt.name]["value"].nb_clause_in += 1
            
        for l in self.backtracking[self.indexBacktracking]["litt_false"]:
            data[l]["value"].setValue(None)
            if "!" in l:
                for clause in data[l]["clause"]:
                    if clause.nb_litt_satisfied > 0:
                        clause.nb_litt_satisfied -= 1
                    if not clause.isSatisfy():
                        if self.nb_clause_satisfy > 0:
                            self.nb_clause_satisfy -= 1
                        for litt in clause.list_litteraux:
                            data[litt.name]["value"].nb_clause_in += 1
            else:
                for clause in data[l]["clause"]:
                    clause.nb_litt_unsatisfied += 1
                    if not clause.isSatisfy():
                        data[l]["value"].nb_clause_in += 1
        self.backtracking.pop()
        self.indexBacktracking -= 1

    def unit_propagate(self, data:dict, litt, clause_empty:list, next_clause_unit:list, litt_false, litt_true):
        if "!" in litt:
            # Met !x à faux
            data[litt]["value"].setValue(False)
            litt_false.append(litt)
        else:
            # Met x à vrai
            data[litt]["value"].setValue(True)
            litt_true.append(litt)
        # Supprime toutes les clauses où x ou !x apparait car elles sont satisfaites
        for clause in data[litt]["clause"]:
            if not clause.isSatisfy():
                self.nb_clause_satisfy += 1
            clause.nb_litt_satisfied += 1
            for l in clause.list_litteraux:
                if l.nb_clause_in > 0:
                    l.nb_clause_in -= 1
        data[litt]["value"].nb_clause_in = 0
          
        if "!" in litt:
            # Met x à faux
            inv_litt = litt.split("!")[1]
            data[inv_litt]["value"].setValue(False)
            litt_false.append(inv_litt)
        else:
            # Met !x à vrai
            inv_litt = "!" + litt
            data[inv_litt]["value"].setValue(True)
            litt_true.append(inv_litt)
        # Supprime x ou !x dans toutes les clauses où il apparait
        for clause in data[inv_litt]["clause"]:
            clause.nb_litt_unsatisfied -= 1
            if clause.isUnit():
                next_clause_unit.append(clause)
            # Si la clause est vide, on la garde en mémoire
            if clause.isNotValid():
                clause_empty[0] = True
        data[inv_litt]["value"].nb_clause_in = 0

    def pure_literal(self, data:dict, litt_true, litt_false):
        all_values = list(data.values())
        for i in range(0,len(all_values), 2):
            x_values = all_values[i]
            notX_values = all_values[i+1]
            if x_values["value"].value == None and notX_values["value"].value:
                if x_values["value"].nb_clause_in == 0 and notX_values["value"].nb_clause_in > 0:
                    notX_values["value"].setValue(False)
                    x_values["value"].setValue(False)
                    litt_false.append(notX_values["value"].name)
                    litt_false.append(x_values["value"].name)
                    # Supprime toutes les clauses où !x apparait car elles sont satisfaites
                    for clause in notX_values["clause"]:
                        if not clause.isSatisfy():
                            self.nb_clause_satisfy += 1
                        clause.nb_litt_satisfied += 1
                        for l in clause.list_litteraux:
                            if l.nb_clause_in > 0:
                                l.nb_clause_in -= 1
                    for clause in x_values["clause"]:
                        clause.nb_litt_unsatisfied -= 1

                elif x_values["value"].nb_clause_in > 0 and notX_values["value"].nb_clause_in == 0:
                    x_values["value"].setValue(True)
                    notX_values["value"].setValue(True)
                    litt_true.append(x_values["value"].name)
                    litt_true.append(notX_values["value"].name)
                    # Supprime toutes les clauses où x apparait car elles sont satisfaites
                    for clause in x_values["clause"]:
                        if not clause.isSatisfy():
                            self.nb_clause_satisfy += 1
                        clause.nb_litt_satisfied += 1
                        for l in clause.list_litteraux:
                            if l.nb_clause_in > 0:
                                l.nb_clause_in -= 1
                    for clause in notX_values["clause"]:
                        clause.nb_litt_unsatisfied -= 1