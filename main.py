from src.app  import App
import numpy as np

if __name__ == '__main__':
    app = App()
    #app.initGui()
    res = app.Dames()
    for a in app.solver.all_solution:
        m = np.zeros((8,8))
        for i in range(1,9):
            for j in range(1,9):
                if a[str.format("x {} {}",i,j)]["value"].value:
                    m[i-1][j-1] = 1
        print(m)
        print("")
    print(len(app.solver.all_solution))