from .generator import Generator
from .dames import Dames
from .solver import Solver
import numpy as np
from PyQt6.QtWidgets import QApplication
from .gui.mainWindow import MainWindow
from .gui.worker import Worker
import os
from .gui.popUp import PopUp
from PyQt6.QtWidgets import QDialogButtonBox

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
        self.game = "Sudoku"
        # Gestion GUI
        self.app = QApplication([])
        self.window = MainWindow()

    def initGui(self):
        self.window.solveButton.clicked.connect(self.handle_solve_click)
        self.window.saveButton.clicked.connect(self.handle_save_click)
        self.window.newButton.clicked.connect(self.handle_new_click)
        self.window.show()
        self.app.exec()

    def createClauseSudoku(self):
        # Creation des clauses
        self.listClause = []
        self.unit_clause = []
        self.data = self.generator.createDict()
        self.generator.genClause(self.data, self.listClause)
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
        self.initSolver()
    
    def createClauseDames(self):
        # Creation des clauses
        self.listClause = []
        self.unit_clause = []
        self.data = self.generatorDames.createDict()
        self.generatorDames.genClause(self.data, self.listClause)
        if self.solver.heuristic == 4:
            moms_data = {
                "2":[],
                str(self.generatorDames.size):[]
            }
            for clause in self.listClause:
                if len(clause.list_litteraux) == 2:
                    moms_data["2"].append(clause)
                elif len(clause.list_litteraux) == 9:
                    moms_data[str(self.generatorDames.size)].append(clause)
            self.solver.moms_data = moms_data

        print("Le nombre de variable propositionnelles est de {} et le nombre de clause est de {}".format(int(self.data.__len__()/2),self.listClause.__len__()))
        self.initSolver()

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
            if not self.window.button_solve_is_clicked:
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
        if not self.window.button_solve_is_clicked:
            self.addClause = []
            self.window.handle_new_click()
    
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
        f.write("Branche clause: " + str(result["close"]) +"\n")
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