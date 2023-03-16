from .generator import Generator
from .solver import Solver
import numpy as np
import time

class App:
    def __init__(self):
        self.generator = Generator()
        self.solver = Solver()
        self.data = None
        self.listClause = []

    def createClause(self):
        # Creation des clauses
        self.data = self.generator.createDict()
        self.generator.genClause(self.data, self.listClause)
        print("Le nombre de variable propositionnelles est de {} et le nombre de clause est de {}".format(int(self.data.__len__()/2),self.listClause.__len__()))
        self.addClauseForNumber()

    def resolve(self):
        start_time = time.time()
        start_time_cpu = time.process_time()
        # Résolution du sudoku
        result_dpll = self.solver.dpll(self.data)
        end_time = time.time()
        end_time_cpu = time.process_time()
        print("Temps d'execution: %s secondes" % np.round((end_time - start_time),2))
        print("Temps d'execution cpu: %s secondes" % np.round((end_time_cpu - start_time_cpu),2))
        if not result_dpll:
            print("Pas de modele")
        else:
            print("Un modele")
        
        # Affichage de la grille finale de sudoku
        self.display_result(result_dpll)

    def addClauseForNumber(self):
        list_litt = [    "x 1 1 8", "x 8 1 7", "x 3 2 6", "x 5 2 1", "x 8 2 5", "x 9 2 3", "x 2 3 4", "x 4 3 6", "x 5 4 8", "x 7 4 4", "x 3 5 3", "x 7 5 7", 
                    "x 2 6 2", "x 6 6 5", "x 8 6 3","x 9 6 8", "x 7 7 8", "x 3 8 4", "x 5 8 5", "x 8 8 6", "x 9 8 1", "x 1 9 9", "x 6 9 2"]
        self.generator.createNumberClause(list_litt, self.data, self.listClause)

    def display_result(self, result_dpll:dict):
        m = np.zeros((9,9))
        for i in range(1,10):
            for j in range(1,10):
                for k in range(1,10):
                    if result_dpll[str.format("x {} {} {}",i,j,k)]["value"].value:
                        m[j-1][i-1] = k
                        break
        print(m)