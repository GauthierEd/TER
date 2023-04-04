from .generator import Generator
from .dames import Dames
from .solver import Solver
import numpy as np
from PyQt6.QtWidgets import QApplication
from .gui.mainWindow import MainWindow
from .gui.worker import Worker
import os
import time
from .gui.popUp import PopUp
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

class App:
    def __init__(self):
        self.generator = Generator()
        self.generatorDames = Dames(8)
        self.solver = Solver()
        self.data = None
        self.result_dpll = None
        self.listClause = []
        self.addClause = []
        self.unit_clause = []
        self.data_etude = {}
        self.game = "Sudoku"
        # Gestion GUI
        self.app = QApplication([])
        self.window = MainWindow()

    def initGui(self):
        self.window.solveButton.clicked.connect(self.handle_solve_click)
        self.window.saveButton.clicked.connect(self.handle_save_click)
        self.window.newButton.clicked.connect(self.handle_new_click)
        self.window.etudeButton.clicked.connect(self.handle_etude_click)
        self.window.show()
        self.app.exec()

    def createClauseSudoku(self):
        # Creation des clauses
        self.listClause = []
        self.unit_clause = []
        self.data = self.generator.createDict()
        self.generator.genClause(self.data, self.listClause)
        self.initSolver()
        if self.solver.heuristic == 4:
            moms_data = {
                "2":[],
                "9":[]
            }
            for clause in self.listClause:
                if len(clause.list_litteraux) == 2:
                    moms_data["2"].append(clause)
                elif len(clause.list_litteraux) == 9:
                    moms_data["9"].append(clause)
            self.solver.moms_data = moms_data

        print("Le nombre de variable propositionnelles est de {} et le nombre de clause est de {}".format(int(self.data.__len__()/2),self.listClause.__len__()))
        if len(self.addClause) > 0:
            self.addClauseForNumber()
        
    
    def createClauseDames(self):
        # Creation des clauses
        self.listClause = []
        self.unit_clause = []
        self.data = self.generatorDames.createDict()
        self.generatorDames.genClause(self.data, self.listClause)
        self.initSolver()
        if self.solver.heuristic == 4:
            moms_data = {
                "2":[],
                str(self.generatorDames.size):[]
            }
            for clause in self.listClause:
                if len(clause.list_litteraux) == 2:
                    moms_data["2"].append(clause)
                elif len(clause.list_litteraux) == self.generatorDames.size:
                    moms_data[str(self.generatorDames.size)].append(clause)
            self.solver.moms_data = moms_data
        print("Le nombre de variable propositionnelles est de {} et le nombre de clause est de {}".format(int(self.data.__len__()/2),self.listClause.__len__()))
        

    def initSolver(self):
        self.solver.nb_clause = len(self.listClause)
        self.solver.backtracking = []
        self.solver.all_solution = []
        self.solver.indexBacktracking = -1
        self.solver.nb_clause_satisfy = 0
        self.solver.recursivity = 0
        self.solver.branch_close = 0
        if self.game == "Dames":
            self.solver.size_max = self.generatorDames.size
        elif self.game == "Sudoku":
            self.solver.size_max = 9

    def reprDames(self, size:int, data:dict):
        m = np.zeros((size,size))
        for i in range(1,size+1):
            for j in range(1,size+1):
                if data[str.format("x {} {}",i,j)]["value"].value:
                    m[i-1][j-1] = 1
        return m

    def reprSudoku(self, data):
        m = np.zeros((9,9))
        for i in range(1,10):
            for j in range(1,10):
                for k in range(1,10):
                    if data[str.format("x {} {} {}",i,j,k)]["value"].value:
                        m[j-1][i-1] = k
        return m
    
    def display_result_dames(self, result):
        print("Temps d'execution: %s secondes" % result["time"])
        print("Temps d'execution cpu: %s secondes" % result["cpu_time"])
        if not self.solver.get_all_solution and result["dpll"]:  
            print("Un modele")
        elif self.solver.get_all_solution and len(self.solver.all_solution) > 0:
            print(len(self.solver.all_solution), " modeles")
        else:
            print("Pas de modele")
        print("Recursivité",self.solver.recursivity)
        print("Branche close",self.solver.branch_close)
        if not self.solver.get_all_solution:
            pass
            #self.window.display_result(result["dpll"])
        else:
            #self.window.display_result(self.solver.all_solution[0])
            for sol in self.solver.all_solution:
                print(self.reprDames(self.generatorDames.size, sol))
                

    def display_result_sudoku(self, result):
        print("Temps d'execution: %s secondes" % result["time"])
        print("Temps d'execution cpu: %s secondes" % result["cpu_time"])
        if not self.solver.get_all_solution and result["dpll"]:  
            print("Un modele")
        elif self.solver.get_all_solution and len(self.solver.all_solution) > 0:
            print(len(self.solver.all_solution), " modeles")
        else:
            print("Pas de modele")
        print("Recursivité",self.solver.recursivity)
        print("Branche close",self.solver.branch_close)
        popup = PopUp(self.window)
        button = popup.exec()
        if button:
            data = {
                "time": result["time"],
                "time_cpu": result["cpu_time"],
                "recursivite": self.solver.recursivity,
                "close": self.solver.branch_close,
                "heuristic": self.solver.heuristic
            }
            if self.solver.get_all_solution:
                data["nb_sol"] = len(self.solver.all_solution)
                if len(self.solver.all_solution) > 0:
                    data["solution"] = self.solver.all_solution
                else:
                    data["solution"] = None
            else:
                if result["dpll"]:
                    data["nb_sol"] = 1
                    data["solution"] = [result["dpll"]]
                else:
                    result["nb_sol"] = 0
                    result["solution"] = None
            self.save(data)

        if not self.solver.get_all_solution:
            self.window.display_result(result["dpll"])
        else:
            self.window.display_result(self.solver.all_solution[0])
            for sol in self.solver.all_solution:
                print(self.reprSudoku(sol))



    def thread_complete(self):
        self.window.button_solve_is_clicked = False

    def resolveSudoku(self):
        # Résolution du sudoku
        worker = Worker(self.solver.dpll, self.data, self.unit_clause)
        worker.signals.result.connect(self.display_result_sudoku)
        worker.signals.finished.connect(self.thread_complete)
        self.window.threadpool.start(worker)

    def resolveDames(self):
        # Résolution du sudoku
        worker = Worker(self.solver.dpll, self.data, self.unit_clause)
        worker.signals.result.connect(self.display_result_dames)
        worker.signals.finished.connect(self.thread_complete)
        self.window.threadpool.start(worker)
        
    def addClauseForNumber(self):
        self.generator.createNumberClause(self.addClause, self.data, self.unit_clause)
    
    def handle_solve_click(self):
        if self.game == "Sudoku":
            if not self.window.button_solve_is_clicked and not self.window.button_etude_is_clicked:
                self.window.button_solve_is_clicked = True
                all_sol = self.window.checkBox.isChecked()
                heuristic = self.window.comboBox.currentText()
                self.solver.set_all_solution(all_sol)
                self.solver.set_heuristic(int(heuristic))
                self.createClauseSudoku()
                self.resolveSudoku()

        elif self.game == "Dames":
            if not self.window.button_solve_is_clicked:
                self.window.button_solve_is_clicked = True
                all_sol = self.window.checkBox.isChecked()
                heuristic = self.window.comboBox.currentText()
                #self.solver.set_all_solution(all_sol)
                #self.solver.set_heuristic(int(heuristic))
                self.createClauseDames()
                self.resolveDames()

    def handle_save_click(self):
        self.window.handle_save_click(self.addClause)
    
    def handle_new_click(self):
        if not self.window.button_solve_is_clicked and not self.window.button_etude_is_clicked:
            self.addClause = []
            self.window.handle_new_click()

    def handle_etude_click(self):
        data = self.load_data("sudoku_facile","sudoku_moyen","sudoku_difficile","sudoku_expert","sudoku_diabolique")
        data_etude = {}
        result = {}
        for key, value in data.items():
            data_heuri = {}
            for i in range(1,7):
                data_heuri[str(i)] = []
            for d in value:
                for i in range(1,7):
                    self.solver.set_all_solution(False)
                    self.solver.set_heuristic(i)
                    self.addClause = d
                    self.createClauseSudoku()
                    start_time = time.time()
                    start_time_cpu = time.process_time()
                    self.solver.dpll(data=self.data, clause_unit=self.unit_clause)
                    end_time = time.time()
                    end_time_cpu = time.process_time()
                    data = {
                        "time": (end_time - start_time),
                        "cpu_time": (end_time_cpu - start_time_cpu),
                        "recursivite": self.solver.recursivity,
                        "branche_close": self.solver.branch_close
                    }
                    data_heuri[str(i)].append(data)
                data_etude[key] = data_heuri
        for key, value in data_etude.items():
            temp = {}
            for h, v in value.items():
                timeTotal = 0
                timeCpuTotal = 0
                recursiviteTotal = 0
                brancheClose = 0
                for data in v:
                    timeTotal += data["time"]
                    timeCpuTotal += data["cpu_time"]
                    recursiviteTotal +=  data["recursivite"]
                    brancheClose += data["branche_close"]
                temp[h] = {
                    'time': timeTotal / len(v),
                    'cpu_time': timeCpuTotal / len(v),
                    'recursivite': recursiviteTotal / len(v),
                    'branche_close': brancheClose / len(v)
                }
            result[key] = temp
        levelV = []
        heuriV = []
        timeV = []
        cpu_timeV = []
        recursivityV = []
        branche_closeV = []
        for level, levelValue in result.items():
            for heuri, heuriValue in levelValue.items():
                levelV.append(level)
                heuriV.append(heuri)
                timeV.append(heuriValue["time"])
                cpu_timeV.append(heuriValue["cpu_time"])
                recursivityV.append(heuriValue["recursivite"])
                branche_closeV.append(heuriValue["branche_close"])
        df = pd.DataFrame({"niveau": levelV, 
                                "heuristique": heuriV,
                                "time": timeV,
                                "cpu_time": cpu_timeV,
                                "recursivite": recursivityV,
                                "branche_close": branche_closeV
                                })
        script_dir = os.path.dirname(__file__)
        abs_file_path = os.path.join(script_dir, "../etude.csv")
        df.to_csv(abs_file_path, index=False)

    def save(self, result):
        script_dir = os.path.dirname(__file__)
        abs_file_path = os.path.join(script_dir, "../solution_"+self.game+".txt")
        if os.path.exists(abs_file_path):
            os.remove(abs_file_path)
        f = open(abs_file_path, 'w')
        f.write("Solution \n")
        f.write("Temps d'execution: "+ str(result["time"]) + " secondes \n")
        f.write("Temps d'execution cpu: "+ str(result["time_cpu"]) + " secondes \n")
        f.write("Heuristique: " + str(result["heuristic"]) + "\n")
        f.write("Recursivite: " + str(result["recursivite"]) + "\n")
        f.write("Branche close: " + str(result["close"]) +"\n")
        f.write("Nombre de solution: " + str(result["nb_sol"])+"\n")
        if result["solution"]:
            f.write("##############################\n\n")
            if self.game == "Dames":
                for i in range(len(result["solution"])):
                    f.write("Solution " + str(i+1) + "\n")
                    m = self.reprDames(self.generatorDames.size, result["solution"][i])
                    self.writeSolution(f, m)

            elif self.game == "Sudoku":
                for i in range(len(result["solution"])):
                    f.write("Solution " + str(i+1) + "\n")
                    m = self.reprSudoku(result["solution"][i])
                    self.writeSolution(f, m)
        f.close()

    def writeSolution(self, file, data):
        for row in data:
            sep = " "
            rowStr = " "
            for i in range(len(row)):
                sep += "----"
                rowStr += "| "+str(int(row[i])) + " "
                if i == len(row) - 1:
                    sep += "-\n"
                    rowStr += "|\n"
            file.write(sep)
            file.write(rowStr)
        file.write("\n")
    
    def load_data(self, *filename):
        script_dir = os.path.dirname(__file__)
        data = {}
        for file in filename:
            level = file.split("_")[1]
            abs_file_path = os.path.join(script_dir, "../sudoku/"+file+".txt")
            f = open(abs_file_path, 'r')
            all_sudoku = []
            content = f.readlines()
            for i in range(0,len(content), 10):
                sudoku = content[i+1:i+10]
                all_sudoku.append(self.get_clue_sudoku(sudoku))
            data[level] = all_sudoku
        return data
    
    def get_clue_sudoku(self, sudoku):
        all_clue = []
        for i in range(len(sudoku)):
            row_split = sudoku[i].split(" ")
            row_split[-1] = row_split[-1].split("\n")[0]
            for j in range(len(row_split)):
                value = int(row_split[j])
                if value != 0:
                    all_clue.append("x "+str(j+1)+" "+str(i+1)+" "+str(value))
        return all_clue