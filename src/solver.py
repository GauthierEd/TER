from copy import deepcopy
from .utils import Clause

class Solver:
    def __init__(self, heuristic = 1):
        self.heuristic = heuristic
        self.all_solution = []

    def dpll(self, data:dict, litteral = None):
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
        
        result = self.dpll(deepcopy(data), new_litteral)
        if result:
            return result
        result = self.dpll(deepcopy(data), "!"+new_litteral)
        if result:
            return result
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
        for clause in data[litt]["clause"]:
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
        for clause in data[inv_litt]["clause"]:
            # On supprimer aussi x des autres clauses car ils sont passé en copy dans le dict
            clause.list_litteraux = list(clause.list_litteraux)
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