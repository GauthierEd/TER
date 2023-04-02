from PyQt6.QtCore import QSize, Qt, QRect, QThreadPool
from PyQt6.QtWidgets import QComboBox, QCheckBox, QLineEdit, QMainWindow, QStackedLayout, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpacerItem
from PyQt6.QtGui import QFont, QIntValidator, QValidator
from .grid import Grid
from .gridEdit import GridEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.button_solve_is_clicked = False
        self.setFixedSize(QSize(600, 600))
        self.centralwidget = QWidget(parent=self)
        self.verticalLayoutWidget_4 = QWidget(parent=self.centralwidget)
        self.verticalLayoutWidget_4.setGeometry(QRect(0, 0, 600, 600))

        self.stackedLayout = QStackedLayout(self.verticalLayoutWidget_4)

        self.first = QWidget()
        self.verticalLayout_4 = QVBoxLayout(self.first)
        self.verticalLayout_4.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_4.setSpacing(0)

        # BUTTON TOP
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(50, 0, 50, 0)
        self.horizontalLayout_3.setSpacing(20)
        font = QFont()
        font.setPointSize(20)
        
        self.newButton = QPushButton("New")
        self.newButton.setFont(font)
        self.horizontalLayout_3.addWidget(self.newButton)

        self.editButton = QPushButton("Edit")
        self.editButton.setFont(font)
        self.editButton.clicked.connect(self.handle_edit_click)
        self.horizontalLayout_3.addWidget(self.editButton)

        self.solveButton = QPushButton("Solve")
        self.solveButton.setFont(font)
        self.horizontalLayout_3.addWidget(self.solveButton)

        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(50, 0, 50, 0)
        self.horizontalLayout_5.setSpacing(20)

        self.checkBox = QCheckBox("Toutes les solutions")
        self.horizontalLayout_5.addWidget(self.checkBox)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(70, 10, 70, 0)
        self.horizontalLayout_6.setSpacing(5)
        self.labelSpinBox = QLabel("Heuristique :")
        self.horizontalLayout_6.addWidget(self.labelSpinBox)
        self.comboBox = QComboBox()
        self.comboBox.addItem("1")
        self.comboBox.addItem("2")
        self.comboBox.addItem("3")
        self.comboBox.addItem("4")
        self.comboBox.addItem("5")
        self.comboBox.addItem("6")
        self.horizontalLayout_6.addWidget(self.comboBox)

        self.horizontalLayout_5.addLayout(self.horizontalLayout_6)

        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        # SPACE SEPARATOR
        spacerItem = QSpacerItem(5, 20)
        self.verticalLayout_4.addItem(spacerItem)

        # GRID BOTTOM
        self.grid = [[0 for x in range(9)] for y in range(9)]
        for i in range(9):
            for j in range(9):
                label = QLabel("")
                label.setGeometry(QRect(0, 0, 55, 50))
                label.setFont(font)
                label.setStyleSheet("background-color:\"#cccdcf\"")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.grid[i][j] = label 
        
        self.gridSudoku = Grid(self.grid, self.first)
    
        self.verticalLayout_4.addLayout(self.gridSudoku)
        self.stackedLayout.addWidget(self.first)

        self.second = QWidget()
        self.verticalLayout_5 = QVBoxLayout(self.second)
        self.verticalLayout_5.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_5.setSpacing(0)
        # BUTTON TOP
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(50, 0, 50, 0)
        self.horizontalLayout_4.setSpacing(20)
        
        self.saveButton = QPushButton("Save")
        self.saveButton.setFont(font)
        self.horizontalLayout_4.addWidget(self.saveButton)

        self.returnButton = QPushButton("Return")
        self.returnButton.setFont(font)
        self.returnButton.clicked.connect(self.handle_return_click)
        self.horizontalLayout_4.addWidget(self.returnButton)

        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        # SPACE SEPARATOR
        spacerItem = QSpacerItem(5, 20)
        self.verticalLayout_5.addItem(spacerItem)

        self.gridInput = [[0 for x in range(9)] for y in range(9)]
        onlyInt = Validator()
        for i in range(9):
            for j in range(9):
                input = QLineEdit()
                input.setValidator(onlyInt)
                input.setFixedWidth(55)
                input.setFixedHeight(50)
                input.setFont(font)
                input.setStyleSheet("background-color:\"#cccdcf\"")
                input.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.gridInput[i][j] = input
                
        
        self.gridEdit = GridEdit(self.gridInput, self.second)
        self.verticalLayout_5.addLayout(self.gridEdit)

        self.stackedLayout.addWidget(self.second)
        self.setCentralWidget(self.centralwidget)


    def display_result(self, result):
        for i in range(1,10):
            for j in range(1,10):
                for k in range(1,10):
                    if result[str.format("x {} {} {}",i,j,k)]["value"].value:
                        self.grid[j-1][i-1].setText(str(k))
                        self.gridInput[j-1][i-1].setText(str(k))
                        break

    def handle_new_click(self):
        for i in range(9):
            for j in range(9):
                self.grid[i][j].setText("")
                self.gridInput[i][j].clear()
        

    def handle_edit_click(self):
        if not self.button_solve_is_clicked:
            self.stackedLayout.setCurrentIndex(1)

    def handle_save_click(self, list_clause):
        for i in range(9):
            for j in range(9):
                if self.gridInput[i][j].text():
                    clause = str.format("x {} {} {}",j+1,i+1,self.gridInput[i][j].text())
                    list_clause.append(clause)
                self.grid[i][j].setText(self.gridInput[i][j].text())
        self.stackedLayout.setCurrentIndex(0)

    def handle_return_click(self):
        self.stackedLayout.setCurrentIndex(0)

class Validator(QIntValidator):
    def __init__(self):
        super().__init__()
        self.setRange(1,9)

    def validate(self, ch, pos):
        if pos==1 and ch=="0":
            return (QValidator.State.Invalid, ch, pos)
        return QIntValidator.validate(self, ch, pos)