from .generator import Generator
from .solver import Solver
import numpy as np
import time
from PyQt6.QtWidgets import QApplication
from .gui.mainWindow import MainWindow
from .gui.worker import Worker

class App:
    def __init__(self):
        self.generator = Generator()
        self.solver = Solver()
        self.data = None
        self.result_dpll = None
        self.listClause = []
        self.addClause = []
        # Gestion GUI
        self.app = QApplication([])
        self.window = MainWindow()

    def initGui(self):
        self.window.solveButton.clicked.connect(self.handle_solve_click)
        self.window.saveButton.clicked.connect(self.handle_save_click)
        self.window.newButton.clicked.connect(self.handle_new_click)
        self.window.show()
        self.app.exec()

    def createClause(self):
        # Creation des clauses
        self.listClause = []
        self.data = self.generator.createDict()
        self.generator.genClause(self.data, self.listClause)
        print("Le nombre de variable propositionnelles est de {} et le nombre de clause est de {}".format(int(self.data.__len__()/2),self.listClause.__len__()))
        if len(self.addClause) > 0:
            self.addClauseForNumber()

    def display_result(self, result):
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
            self.window.display_result(result["dpll"])
        else:
            self.window.display_result(self.solver.all_solution[0])
            for a in self.solver.all_solution:
                m = np.zeros((9,9))
                for i in range(1,10):
                    for j in range(1,10):
                        for k in range(1,10):
                            if a[str.format("x {} {} {}",i,j,k)]["value"].value:
                                m[j-1][i-1] = k
                print(m)

    def thread_complete(self):
        self.window.button_solve_is_clicked = False

    def resolve(self):
        # Résolution du sudoku
        worker = Worker(self.solver.dpll, self.data)
        worker.signals.result.connect(self.display_result)
        worker.signals.finished.connect(self.thread_complete)
        self.window.threadpool.start(worker)
        
    def addClauseForNumber(self):
        self.generator.createNumberClause(self.addClause, self.data, self.listClause)
    
    def handle_solve_click(self):
        if not self.window.button_solve_is_clicked:
            self.window.button_solve_is_clicked = True
            all_sol = self.window.checkBox.isChecked()
            heuristic = self.window.comboBox.currentText()
            self.solver.set_all_solution(all_sol)
            self.solver.set_heuristic(int(heuristic))
            self.solver.all_solution = []
            self.createClause()
            self.resolve()

    def handle_save_click(self):
        self.window.handle_save_click(self.addClause)
    
    def handle_new_click(self):
        if not self.window.button_solve_is_clicked:
            self.addClause = []
            self.window.handle_new_click()