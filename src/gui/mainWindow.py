from PyQt6.QtCore import QSize, Qt, QRect
from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QPalette, QColor, QFont
from copy import deepcopy

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setFixedSize(QSize(600, 600))
        self.centralwidget = QWidget(parent=self)
        self.verticalLayoutWidget_4 = QWidget(parent=self.centralwidget)
        self.verticalLayoutWidget_4.setGeometry(QRect(0, 0, 600, 600))

        self.verticalLayout_4 = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_4.setSpacing(0)

        # BUTTON TOP
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(50, 0, 50, 0)
        self.horizontalLayout_3.setSpacing(20)
        font = QFont()
        font.setPointSize(20)
        
        self.editButton = QPushButton("Edit")
        self.editButton.setFont(font)
        self.horizontalLayout_3.addWidget(self.editButton)

        self.solveButton = QPushButton("Solve")
        self.solveButton.setFont(font)
        #self.solveButton.clicked.connect(self.handle_solve_click)
        self.horizontalLayout_3.addWidget(self.solveButton)

        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        # SPACE SEPARATOR
        spacerItem = QSpacerItem(5, 20)
        self.verticalLayout_4.addItem(spacerItem)

        # GRID BOTTOM
        self.grid = [[0 for x in range(10)] for y in range(10)] 
        for i in range(10):
            for j in range(10):
                label = QLabel("")
                label.setFont(font)
                label.setStyleSheet("background-color:\"#cccdcf\"")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.grid[i][j] = label
        self.horizontalLayout = QHBoxLayout()
        self.verticalLayout = QVBoxLayout()
        #   X - -
        #   - - -
        #   - - -
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setContentsMargins(0, 0, 4, 4)
        self.gridLayout_4.setSpacing(4)
        for i in range(3):
            for j in range(3):
                self.gridLayout_4.addWidget(self.grid[i][j], i, j)
        self.verticalLayout.addLayout(self.gridLayout_4)

        self.line_2 = QFrame(parent=self.verticalLayoutWidget_4)
        self.line_2.setFrameShadow(QFrame.Shadow.Plain)
        self.line_2.setLineWidth(3)
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.verticalLayout.addWidget(self.line_2)

        #   - - -
        #   X - -
        #   - - -
        self.gridLayout = QGridLayout()
        self.gridLayout.setContentsMargins(0, 4, 4, 4)
        self.gridLayout.setSpacing(4)
        for i in range(3):
            for j in range(3):
                self.gridLayout.addWidget(self.grid[i+3][j], i, j)
        self.verticalLayout.addLayout(self.gridLayout)

        self.line = QFrame(parent=self.verticalLayoutWidget_4)
        self.line.setFrameShadow(QFrame.Shadow.Plain)
        self.line.setLineWidth(3)
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.verticalLayout.addWidget(self.line)

        #   - - -
        #   - - -
        #   X - -
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setContentsMargins(0, 4, 4, 0)
        self.gridLayout_3.setSpacing(4)
        for i in range(3):
            for j in range(3):
                self.gridLayout_3.addWidget(self.grid[i+6][j], i, j)
        self.verticalLayout.addLayout(self.gridLayout_3)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.line_7 = QFrame(parent=self.verticalLayoutWidget_4)
        self.line_7.setFrameShadow(QFrame.Shadow.Plain)
        self.line_7.setLineWidth(3)
        self.line_7.setFrameShape(QFrame.Shape.VLine)
        self.horizontalLayout.addWidget(self.line_7)

        self.verticalLayout_2 = QVBoxLayout()
        
        #   - X -
        #   - - -
        #   - - -
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setContentsMargins(4, 0, 4, 4)
        self.gridLayout_5.setSpacing(4)
        for i in range(3):
            for j in range(3):
                self.gridLayout_5.addWidget(self.grid[i][j+3], i, j)
        self.verticalLayout_2.addLayout(self.gridLayout_5)

        self.line_3 = QFrame(parent=self.verticalLayoutWidget_4)
        self.line_3.setFrameShadow(QFrame.Shadow.Plain)
        self.line_3.setLineWidth(3)
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.verticalLayout_2.addWidget(self.line_3)

        #   - - -
        #   - X -
        #   - - -
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_6.setSpacing(4)
        for i in range(3):
            for j in range(3):
                self.gridLayout_6.addWidget(self.grid[i+3][j+3], i, j)
        self.verticalLayout_2.addLayout(self.gridLayout_6)

        self.line_4 = QFrame(parent=self.verticalLayoutWidget_4)
        self.line_4.setFrameShadow(QFrame.Shadow.Plain)
        self.line_4.setLineWidth(3)
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.verticalLayout_2.addWidget(self.line_4)

        #   - - -
        #   - - -
        #   - X -
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setContentsMargins(4, 4, 4, 0)
        self.gridLayout_7.setSpacing(4)
        for i in range(3):
            for j in range(3):
                self.gridLayout_7.addWidget(self.grid[i+6][j+3], i, j)
        self.verticalLayout_2.addLayout(self.gridLayout_7)

        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.line_8 = QFrame(parent=self.verticalLayoutWidget_4)
        self.line_8.setFrameShadow(QFrame.Shadow.Plain)
        self.line_8.setLineWidth(3)
        self.line_8.setFrameShape(QFrame.Shape.VLine)
        self.horizontalLayout.addWidget(self.line_8)

        self.verticalLayout_3 = QVBoxLayout()
        #   - - X
        #   - - -
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setContentsMargins(4, 0, 0, 4)
        self.gridLayout_8.setSpacing(4)
        for i in range(3):
            for j in range(3):
                self.gridLayout_8.addWidget(self.grid[i][j+6], i, j)
        self.verticalLayout_3.addLayout(self.gridLayout_8)

        self.line_5 = QFrame(parent=self.verticalLayoutWidget_4)
        self.line_5.setFrameShadow(QFrame.Shadow.Plain)
        self.line_5.setLineWidth(3)
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.verticalLayout_3.addWidget(self.line_5)

        #   - - -
        #   - - X
        #   - - -
        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setContentsMargins(4, 4, 0, 4)
        self.gridLayout_9.setSpacing(4)
        for i in range(3):
            for j in range(3):
                self.gridLayout_9.addWidget(self.grid[i+3][j+6], i, j)
        self.verticalLayout_3.addLayout(self.gridLayout_9)

        self.line_6 = QFrame(parent=self.verticalLayoutWidget_4)
        self.line_6.setFrameShadow(QFrame.Shadow.Plain)
        self.line_6.setLineWidth(3)
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.verticalLayout_3.addWidget(self.line_6)

        #   - - -
        #   - - -
        #   - - X
        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setContentsMargins(4, 4, 0, 0)
        self.gridLayout_10.setSpacing(4)
        for i in range(3):
            for j in range(3):
                self.gridLayout_10.addWidget(self.grid[i+6][j+6], i, j)
        self.verticalLayout_3.addLayout(self.gridLayout_10)

        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.setCentralWidget(self.centralwidget)

    def display_result(self, result):
        for i in range(1,10):
            for j in range(1,10):
                for k in range(1,10):
                    if result[str.format("x {} {} {}",i,j,k)]["value"].value:
                        self.grid[j-1][i-1].setText(str(k))
                        break