from src.app  import App
import time

if __name__ == '__main__':
    app = App()
    print("Quel jeu: Sudoku (1) ou Dames (2) ?")
    choice = input()
    if choice == "1":
        app.game = "Sudoku"
        app.initGui()
    elif choice == "2":
        app.game = "Dames"
        print("Taille de l'échiquier ?")
        size = input()
        app.generatorDames.size = int(size)
        print("Trouver toutes les solutions (y/n) ? ")
        sol = input()
        if sol == "y":
            app.solver.set_all_solution(True)
        else:
            app.solver.set_all_solution(False)
        print("Quelle heuristiques utiliser (entre 1 et 6) ?")
        heuristic = input()
        app.solver.set_heuristic(int(heuristic))
        app.createClauseDames()
        start_time = time.time()
        start_time_cpu = time.process_time()
        res = app.solver.dpll(app.data)
        end_time = time.time()
        end_time_cpu = time.process_time()
        print("Voulez vous sauvegarder la solution ? (y/n) :")
        sol = input()
        if sol == "y":
            result = {
                "time": (end_time-start_time),
                "time_cpu": (end_time_cpu-start_time_cpu),
                "recursivite": app.solver.recursivity,
                "close": app.solver.branch_close,
                "heuristic": app.solver.heuristic
            }
            if app.solver.get_all_solution:
                result["nb_sol"] = len(app.solver.all_solution)
                if len(app.solver.all_solution) > 0:
                    result["solution"] = app.solver.all_solution
                else:
                    result["solution"] = None
            else:
                if res:
                    result["nb_sol"] = 1
                    result["solution"] = [res]
                else:
                    result["nb_sol"] = 0
                    result["solution"] = None
            app.save(result)
        else:
            print("Temps d'execution: %s secondes" % (end_time-start_time))
            print("Temps d'execution cpu: %s secondes" % (end_time_cpu-start_time_cpu))
            print("Recursivité",app.solver.recursivity)
            print("Branche close",app.solver.branch_close)
            if app.solver.get_all_solution:
                if len(app.solver.all_solution) > 0:
                    for data in app.solver.all_solution:
                        print(app.reprDames(int(size), data))
                        print("")
                    print("Nombre de solutions :",len(app.solver.all_solution))
                else:
                    print("Pas de solution")
            else:
                if res:
                    print(app.reprDames(int(size), res))
                else:
                    print("Pas de solution")  