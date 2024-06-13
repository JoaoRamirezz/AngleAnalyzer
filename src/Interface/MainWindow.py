import os
import Backend.Connection as backend
from PyQt5.QtGui import *
from .ConfigWindow import ConfigWindow
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from .style.InterfaceStyle import *
from Backend.ConfigJson import ConfigJson



class MainWindow(QWidget):
    
    def __init__(self):
        self.config = ConfigJson()
        self.jsonPath = self.config.read()["Path"]
        
        #region SCREEN CONFIGS
        super().__init__()
        self.setWindowTitle("Angle Analyzer")
        self.resize(350,300)
        self.layout = QVBoxLayout()
        
        iconPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../images/Icon_Angle.png'))
        self.setWindowIcon(QIcon(iconPath))
        #endregion
        
        
        #region VARIABLES
        self.line = False
        self.border = False
        self.center = False
        self.adjust = False
        self.searched = False
        #endregion
        
        
        #region SETTING LAYOUTS
        headerLayout = QHBoxLayout()
        headerLayout.setAlignment(Qt.AlignCenter)
        
        checkboxLayout = QHBoxLayout()
        textlimitLayout = QHBoxLayout()
        limitLayout = QHBoxLayout()
        
        pathLayout = QHBoxLayout()
        pathTextLayout = QHBoxLayout()
        analyzerLayout = QHBoxLayout()
        configLayout = QHBoxLayout()
        #endregion
        
        
        #region CHECKBOXES
        self.showAdjust = QCheckBox("Pontos de ajuste")
        self.showAdjust.stateChanged.connect(self.changeAdjust)
        
        self.showLines = QCheckBox("Mostrar Linhas")
        self.showLines.stateChanged.connect(self.changeLine)
        
        self.showBorder = QCheckBox("Mostrar Contorno")
        self.showBorder.stateChanged.connect(self.changeBorder)
        
        self.showCenter = QCheckBox("Mostrar Centro")
        self.showCenter.stateChanged.connect(self.changeCenter)
        
        
        checkboxLayout.addWidget(self.showLines)
        checkboxLayout.addWidget(self.showAdjust)
        checkboxLayout.addWidget(self.showBorder)
        checkboxLayout.addWidget(self.showCenter)
        
        checkboxLayout.setAlignment(Qt.AlignCenter)
        #endregion
        
        
        #region LOGOS
        imagePath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../images/AngleAnalyzer-Logo.png'))
        pixmap = QPixmap(imagePath)
        scaledPixmap = pixmap.scaled(150, 150)
        imageLabel = QLabel()
        imageLabel.setPixmap(scaledPixmap)
        
        imagePath2 = os.path.abspath(os.path.join(os.path.dirname(__file__), '../images/Logo_ENS.png'))
        pixmap = QPixmap(imagePath2)
        scaledPixmap = pixmap.scaled(120, 100)
        imageLabel2 = QLabel()
        imageLabel2.setPixmap(scaledPixmap)
        

        headerLayout.addWidget(imageLabel)
        headerLayout.addWidget(imageLabel2)
        #endregion
        
        
        #region BUTTONS
        self.searchImg = QPushButton("Selecionar Imagem")
        self.searchImg.clicked.connect(self.openFileDialog)
        self.searchFolder = QPushButton("Selecionar Pasta")
        self.searchFolder.clicked.connect(self.openFolderDialog)
        self.path = QLabel("Caminho: " + self.jsonPath)
        
        self.findAngle = QPushButton("Analizar Ângulos")
        self.configScreen = QPushButton("Configurações")
        
        self.findAngle.clicked.connect(self.call_connection)
        self.configScreen.clicked.connect(self.openConfig)

        self.setStyleSheet(style())
        pathLayout.addWidget(self.searchImg)
        pathLayout.addWidget(self.searchFolder)
        pathTextLayout.addWidget(self.path)
        analyzerLayout.addWidget(self.findAngle)
        configLayout.addWidget(self.configScreen)
        #endregion
        
        
        #region INPUTS
        self.goodText = QLabel("Valor ângulo bom")
        self.medianText = QLabel("Valor ângulo medio")
        self.goodInput = QLineEdit()
        self.medianInput = QLineEdit()

        limitLayout.addWidget(self.goodInput)
        limitLayout.addWidget(self.medianInput)
        textlimitLayout.addWidget(self.goodText)
        textlimitLayout.addWidget(self.medianText)
        #endregion
        
        
        #region ADD LAYOUTS
        self.layout.addLayout(headerLayout)
        self.layout.addLayout(checkboxLayout)
        self.layout.addLayout(textlimitLayout)
        self.layout.addLayout(limitLayout)
        self.layout.addLayout(pathLayout)
        self.layout.addLayout(pathTextLayout)
        self.layout.addLayout(analyzerLayout)
        self.layout.addLayout(configLayout)
        self.setLayout(self.layout)
        #endregion
    
    
    #region FUNCTIONS
    def call_connection(self):
        self.searched = True
        backend.run(self.jsonPath, self.goodInput.text(), self.medianInput.text(), self.line, self.border, self.center, self.adjust)
    
    def changeLine(self, state):
        if state == 2:
            self.line = True
        elif state == 0:
            self.line = False
        
        # if self.searched:
        #     backend.run(self.goodInput.text(), self.medianInput.text(), self.line, self.border, self.center, self.lineSize)

    def changeBorder(self, state):
        if state == 2:
            self.border = True
        elif state == 0:
            self.border = False
            
    def changeAdjust(self, state):
        if state == 2:
            self.adjust = True
        elif state == 0:
            self.adjust = False
       
    def changeCenter(self, state):
        if state == 2:
            self.center = True
        elif state == 0:
            self.center = False
            
        # if self.searched:
        #     backend.run(self.goodInput.text(), self.medianInput.text(), self.line, self.border, self.center, self.lineSize)
            
    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a file", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_path:
            self.config.set(0,0,file_path)
            self.jsonPath = self.config.read()["Path"]
            self.path.setText("Caminho: " + self.jsonPath)
            
    def openFolderDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        folder_path = QFileDialog.getExistingDirectory(self, "Select a folder", "", options=options)
        if folder_path:
            self.config.set(0,0,folder_path)
            self.jsonPath = self.config.read()["Path"]
            self.path.setText("Caminho: " + self.jsonPath)
            
    def openConfig(self):
        config = ConfigWindow()
        config.show()
    #endregion