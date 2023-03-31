from copy import deepcopy
from .utils import Clause
import random

class Solver:
    def __init__(self, heuristic = 1):
        self.heuristic = heuristic
        self.all_solution = []
        self.get_all_solution = False
        self.recursivity = 0
        self.branch_close = 0

    def set_all_solution(self, choice):
        self.get_all_solution = choice
        if self.get_all_solution:
            print("Cherche toutes les solutions")
        else:
            print("Cherche une solution")

    def set_heuristic(self,choice):
        self.heuristic = choice
        print("Utilise heuristic", choice)
    
    def get_S_x(self, listC, x):
        k = 2
        occur_x = self.f(listC,x)
        occur_nx = self.f(listC, "!"+x)
        return (occur_x + occur_nx) * pow(2,k) + (occur_x * occur_nx)

    
    def f(self, listC, x):
        # Renvoie le nombre d'occurence d'un litteral dans toutes les plus petites
        # clauses non satisfaites et non unitaire
        occur = 0
        for clause in listC:
            for l in clause.list_litteraux:
                if l.name == x:
                    occur += 1
        return occur

    def dpll(self, data:dict, litteral = None):
        self.recursivity += 1
        clause_empty = []
        clause_uni = []
        if litteral != None:
            clause_uni.append(Clause([data[litteral]["value"]]))
        # Recherche de toutes les clauses unitaires
        for key, value in data.items():
            for clause in value["clause"]:
                if len(clause.list_litteraux) == 1:
                    clause_uni.append(clause)
        
        #### PROPAGATION UNITAIRE ####
        for clause in clause_uni:
            if len(clause.list_litteraux) > 0:
                litt = clause.list_litteraux[0].name
            else:
                break
            self.unit_propagate(data, litt, clause_empty)
        #### LITTERAUX PURE ####
        self.pure_literal(data)
        # Test s'il existe des clauses vides
        if len(clause_empty) > 0:
            self.branch_close += 1
            return False
        
        # Test si il y a plus de clause
        isEmpty = True
        for key, value in data.items():
            if len(value["clause"]) > 0:
                isEmpty = False
        if isEmpty and not self.get_all_solution:
            return data
        elif isEmpty and self.get_all_solution:
            self.all_solution.append(data)
            return True
        
        if self.heuristic == 1:
            # On choisit un litteral, on prends le 1er litteral qui n'a pas encore de valeur associé
            for key, value in data.items():
                if value["value"].value == None and len(value["clause"]) > 0:
                    new_litteral = key
                    break
        elif self.heuristic == 2:
            keys = list(data.keys())
            for k in list(keys):
                if len(data[k]["clause"]) == 0 and data[k]["value"].value != None:
                    keys.remove(k)
            new_litteral = random.choice(keys)
        elif self.heuristic == 3:
            # MOMS Heuristic
            # get smallests clause not satisfied
            # Récupérer toutes les plus petites clauses qui ne sont pas unitaires
            # Prendre le litteral qui a la plus grand occurence dans celle ci
            smallest_clause = []
            size = float('inf')
            for key, value in data.items():
                if value["value"].value == None and len(value["clause"]) > 0:
                    for clause in value["clause"]:
                        length = len(clause.list_litteraux)
                        # pas clause unitaire et plus petit
                        if length > 1 and length < size:
                            smallest_clause = [clause]
                            size = length
                        elif length > 1 and length == size:
                            smallest_clause.append(clause)
            all_litt = list(data.keys())
            maxOccur = 0
            for i in range(0,len(all_litt), 2):               
                litt = all_litt[i]
                litt_occur = self.get_S_x(smallest_clause, litt)
                if litt_occur > maxOccur:
                    maxOccur = litt_occur
                    new_litteral = litt
        if "!" in new_litteral:
            new_litteral = new_litteral.split("!")[1]
        result = self.dpll(deepcopy(data), new_litteral)
        if result and not self.get_all_solution:
            return result
        result = self.dpll(deepcopy(data), "!"+new_litteral)
        if result and not self.get_all_solution:
            return result
        elif result and self.get_all_solution:
            return True
        else:
            return False

    def unit_propagate(self, data:dict, litt, clause_empty:list):
        if "!" in litt:
            # Met !x à faux
            data[litt]["value"].setValue(False)
        else:
            # Met x à vrai
            data[litt]["value"].setValue(True)
        # Supprime toutes les clauses où x ou !x apparait car elles sont satisfaites
        for clause in list(data[litt]["clause"]):
            clause_litt = clause.list_litteraux
            for l in clause_litt:
                data[l.name]["clause"].remove(clause)
                    
        if "!" in litt:
            # Met x à faux
            inv_litt = litt.split("!")[1]
            data[inv_litt]["value"].setValue(False)
        else:
            # Met !x à vrai
            inv_litt = "!" + litt
            data[inv_litt]["value"].setValue(True)
        # Supprime x ou !x dans toutes les clauses où il apparait
        for clause in list(data[inv_litt]["clause"]):
            # On supprimer aussi x des autres clauses car ils sont passé en copy dans le dict
            clause.list_litteraux.remove(data[inv_litt]["value"])
            # Si la clause est vide, on la garde en mémoire
            if len(clause.list_litteraux) == 0:
                clause_empty.append(clause)
        data[inv_litt]["clause"] = []

    def pure_literal(self, data:dict):
        all_values = list(data.values())
        for i in range(0,len(all_values), 2):
            x_values = all_values[i]
            notX_values = all_values[i+1]
            if len(x_values["clause"]) == 0 and len(notX_values["clause"]) > 0:
                notX_values["value"].setValue(False)
                # Supprime toutes les clauses où !x apparait car elles sont satisfaites
                for clause in list(notX_values["clause"]):
                    clause.isSatisfy = True
                    clause_litt = clause.list_litteraux
                    for l in clause_litt:
                        if len(data[l.name]["clause"]) > 0:
                            data[l.name]["clause"].remove(clause)
            elif len(x_values["clause"]) > 0 and len(notX_values["clause"]) == 0:
                x_values["value"].setValue(True)
                # Supprime toutes les clauses où x apparait car elles sont satisfaites
                for clause in list(x_values["clause"]):
                    clause.isSatisfy = True
                    clause_litt = clause.list_litteraux
                    for l in clause_litt:
                        if len(data[l.name]["clause"]) > 0:
                            data[l.name]["clause"].remove(clause)