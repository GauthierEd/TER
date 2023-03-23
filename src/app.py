from .generator import Generator
from .solver import Solver
import numpy as np
import time
from PyQt6.QtWidgets import QApplication
from .gui.mainWindow import MainWindow

class App:
    def __init__(self):
        self.generator = Generator()
        self.solver = Solver()
        self.data = None
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
        self.data = self.generator.createDict()
        self.generator.genClause(self.data, self.listClause)
        print("Le nombre de variable propositionnelles est de {} et le nombre de clause est de {}".format(int(self.data.__len__()/2),self.listClause.__len__()))
        if len(self.addClause) > 0:
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
        if not self.solver.get_all_solution and result_dpll:
            print("Un modele")
        elif self.solver.get_all_solution and len(self.solver.all_solution) > 0:
            print(len(self.solver.all_solution), " modeles")
        else:
            print("Pas de modele")
        # Affichage de la grille finale de sudoku
        if not self.solver.get_all_solution:
            self.window.display_result(result_dpll)
        else:
            self.window.display_result(self.solver.all_solution[0])

    def addClauseForNumber(self):
        list_litt = [    "x 1 1 8", "x 8 1 7", "x 3 2 6", "x 5 2 1", "x 8 2 5", "x 9 2 3", "x 2 3 4", "x 4 3 6", "x 5 4 8", "x 7 4 4", "x 3 5 3", "x 7 5 7", 
                    "x 2 6 2", "x 6 6 5", "x 8 6 3","x 9 6 8", "x 7 7 8", "x 3 8 4", "x 5 8 5", "x 8 8 6", "x 9 8 1", "x 1 9 9", "x 6 9 2"]
        self.generator.createNumberClause(self.addClause, self.data, self.listClause)
    
    def handle_solve_click(self):
        if not self.window.button_solve_is_clicked:
            self.button_solve_is_clicked = True
            all_sol = self.window.checkBox.checkState()
            "CheckState.Unchecked ou CheckState.Checked"
            heuristic = self.window.comboBox.currentText()
            print(all_sol, heuristic)
            self.createClause()
            self.resolve()
            self.window.button_solve_is_clicked = False  

    def handle_save_click(self):
        self.window.handle_save_click(self.addClause)
    
    def handle_new_click(self):
        if not self.window.button_solve_is_clicked:
            self.addClause = []
            self.window.handle_new_click()