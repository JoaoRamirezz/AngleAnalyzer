import os
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from Backend.ConfigJson import ConfigJson
from .style.InterfaceStyle import style
from functools import partial


class ConfigWindow(QWidget):
    def __init__(self):
        self.config = ConfigJson()
        
        #region SCREEN CONFIGS
        super().__init__()
        self.setWindowTitle("Configurações")
        self.resize(350,300)
        self.layout = QVBoxLayout()
        
        iconPath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images/Icon_Angle.png'))
        self.setWindowIcon(QIcon(iconPath))
        #endregion
        
        
        #region PICKUP JSON VALUES
        self.colorDisplays = []
        self.colorValues = self.config.getColors()
        self.widthValues = self.config.getWidths()
        #endregion
        
        
        #region SETTING LAYOUTS
        lines = QHBoxLayout()
        lines.setAlignment(Qt.AlignCenter)
        linesWidth = QHBoxLayout()
        linesColor = QHBoxLayout()
        self.linesGroup = QButtonGroup(self)
        self.linesGroup.setExclusive(True)
    
        borders = QHBoxLayout()
        borders.setAlignment(Qt.AlignCenter)
        bordersWidth = QHBoxLayout()
        bordersColor = QHBoxLayout()
        self.bordersGroup = QButtonGroup(self)
        self.bordersGroup.setExclusive(True)
        
        center = QHBoxLayout()
        center.setAlignment(Qt.AlignCenter)
        centerWidth = QHBoxLayout()
        centerColor = QHBoxLayout()
        self.centerGroup = QButtonGroup(self)
        self.centerGroup.setExclusive(True)
        
        adjust = QHBoxLayout()
        adjust.setAlignment(Qt.AlignCenter)
        adjustWidth = QHBoxLayout()
        adjustColor = QHBoxLayout()
        self.adjustGroup = QButtonGroup(self)
        self.adjustGroup.setExclusive(True)
        #endregion
        
        
        #region LINES
        
        linescheck = []
        
        self.textline = QLabel("Linhas")
        lines.addWidget(self.textline)
        
        self.lineFine = QCheckBox("Fina")
        self.lineMedium = QCheckBox("Media")
        self.lineHard = QCheckBox("Grossa")
        
        linescheck.append(self.lineFine)
        linescheck.append(self.lineMedium)
        linescheck.append(self.lineHard)
        
        linescheck[self.config.read()["Lines Width"]-1].setChecked(True) 
        
        self.linesGroup.addButton(self.lineFine)
        self.linesGroup.addButton(self.lineMedium)
        self.linesGroup.addButton(self.lineHard)
        self.linesGroup.buttonClicked.connect(partial(self.changeWidth, 0))
        
        linesWidth.addWidget(self.lineFine)
        linesWidth.addWidget(self.lineMedium)
        linesWidth.addWidget(self.lineHard)
        
        self.lineColorButton = QPushButton("Escolher cor Linha")
        self.lineColorButton.clicked.connect(partial(self.changeColor, 0))
        
        self.lineColorDisplay = QWidget(self)
        self.lineColorDisplay.setFixedSize(60, 30)
        self.lineColorDisplay.setStyleSheet("QWidget { background-color : rgb"+str(self.colorValues[0])+"; }")
        self.colorDisplays.append(self.lineColorDisplay)
        
        linesColor.addWidget(self.lineColorButton)
        linesColor.addWidget(self.colorDisplays[0])
        #endregion
        
        
        #region BORDERS
        borderscheck = []
        
        self.textborder = QLabel("Bordas")
        borders.addWidget(self.textborder)
        
        self.borderFine = QCheckBox("Fina")
        self.borderMedium = QCheckBox("Media")
        self.borderHard = QCheckBox("Grossa")
        
        borderscheck.append(self.borderFine)
        borderscheck.append(self.borderMedium)
        borderscheck.append(self.borderHard)
        
        borderscheck[self.config.read()["Borders Width"]-1].setChecked(True) 
        
        self.bordersGroup.addButton(self.borderFine)
        self.bordersGroup.addButton(self.borderMedium)
        self.bordersGroup.addButton(self.borderHard)
        self.bordersGroup.buttonClicked.connect(partial(self.changeWidth, 1))
        
        bordersWidth.addWidget(self.borderFine)
        bordersWidth.addWidget(self.borderMedium)
        bordersWidth.addWidget(self.borderHard)
        
        self.borderColorButton = QPushButton("Escolher cor Borda")
        self.borderColorButton.clicked.connect(partial(self.changeColor, 1))
        
        self.borderColorDisplay = QWidget(self)
        self.borderColorDisplay.setFixedSize(60, 30)
        self.borderColorDisplay.setStyleSheet("QWidget { background-color : rgb"+str(self.colorValues[1])+"; }")
        self.colorDisplays.append(self.borderColorDisplay)
        
        bordersColor.addWidget(self.borderColorButton)
        bordersColor.addWidget(self.colorDisplays[1])
        #endregion
        
        
        #region CENTER
        centercheck = []
        
        self.textborder = QLabel("Centro")
        center.addWidget(self.textborder)
        
        self.centerFine = QCheckBox("Pequeno")
        self.centerMedium = QCheckBox("Medio")
        self.centerHard = QCheckBox("Grande")
        
        centercheck.append(self.centerFine)
        centercheck.append(self.centerMedium)
        centercheck.append(self.centerHard)
        
        centercheck[self.config.read()["Center Width"]-1].setChecked(True) 
        
        self.centerGroup.addButton(self.centerFine)
        self.centerGroup.addButton(self.centerMedium)
        self.centerGroup.addButton(self.centerHard)
        self.centerGroup.buttonClicked.connect(partial(self.changeWidth, 2))
        
        centerWidth.addWidget(self.centerFine)
        centerWidth.addWidget(self.centerMedium)
        centerWidth.addWidget(self.centerHard)
        
        self.centerColorButton = QPushButton("Escolher cor Centro")
        self.centerColorButton.clicked.connect(partial(self.changeColor, 2))
        
        self.centerColorDisplay = QWidget(self)
        self.centerColorDisplay.setFixedSize(60, 30)
        self.centerColorDisplay.setStyleSheet("QWidget { background-color : rgb"+str(self.colorValues[2])+"; }")
        self.colorDisplays.append(self.centerColorDisplay)
        
        centerColor.addWidget(self.centerColorButton)
        centerColor.addWidget(self.colorDisplays[2])
        #endregion
        
        
        #region ADJUST
        adjustcheck = []
        
        self.textadjust = QLabel("Ajuste")
        adjust.addWidget(self.textadjust)
        
        self.adjustFine = QCheckBox("Pequeno")
        self.adjustMedium = QCheckBox("Medio")
        self.adjustHard = QCheckBox("Grande")
        
        adjustcheck.append(self.adjustFine)
        adjustcheck.append(self.adjustMedium)
        adjustcheck.append(self.adjustHard)
        
        adjustcheck[self.config.read()["Adjust Width"]-1].setChecked(True) 

        self.adjustGroup.addButton(self.adjustFine)
        self.adjustGroup.addButton(self.adjustMedium)
        self.adjustGroup.addButton(self.adjustHard)
        self.adjustGroup.buttonClicked.connect(partial(self.changeWidth, 3))
        
        adjustWidth.addWidget(self.adjustFine)
        adjustWidth.addWidget(self.adjustMedium)
        adjustWidth.addWidget(self.adjustHard)
        
        self.adjustColorButton = QPushButton("Escolher cor Ajuste")
        self.adjustColorButton.clicked.connect(partial(self.changeColor, 3))
        
        self.adjustColorDisplay = QWidget(self)
        self.adjustColorDisplay.setFixedSize(60, 30)
        self.adjustColorDisplay.setStyleSheet("QWidget { background-color : rgb"+str(self.colorValues[3])+"; }")
        self.colorDisplays.append(self.adjustColorDisplay)
        
        adjustColor.addWidget(self.adjustColorButton)
        adjustColor.addWidget(self.colorDisplays[3])
        #endregion
        
        
        #region SAVE BUTTON
        buttonSave = QHBoxLayout()
        
        self.button = QPushButton("Salvar")
        self.button.clicked.connect(self.AttJson)
        buttonSave.addWidget(self.button)
        #endregion
        
        
        #region ADD LAYOUTS
        self.layout.addLayout(lines)
        self.layout.addLayout(linesWidth)
        self.layout.addLayout(linesColor)
        self.layout.addLayout(borders)
        self.layout.addLayout(bordersWidth)
        self.layout.addLayout(bordersColor)
        self.layout.addLayout(center)
        self.layout.addLayout(centerWidth)
        self.layout.addLayout(centerColor)
        self.layout.addLayout(adjustWidth)
        self.layout.addLayout(adjustColor)
        self.layout.addLayout(buttonSave)
        self.setLayout(self.layout)
        #endregion
        
        
    #region FUNCTIONS
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
    def changeColor(self, index):
        colorPicker = QColorDialog.getColor()
        
        if colorPicker.isValid():
            self.colorValues[index] = self.hex_to_rgb(colorPicker.name())
            self.colorDisplays[index].setStyleSheet(f'QWidget {{ background-color : {colorPicker.name()}; }}')
            
    def changeWidth(self, index, button):
        if button.text() == "Fina" or button.text() == "Pequeno":
            self.widthValues[index] = 1
        elif button.text() == "Media" or button.text() == "Medio":
            self.widthValues[index] = 2
        elif button.text() == "Grossa" or button.text() == "Grande":
            self.widthValues[index] = 3
       
    def AttJson(self):    
        self.config.set(self.widthValues, self.colorValues)
        self.show_popup()
        
    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Salvo")
        msg.setText("As configurações foram salvas!")
        x = msg.exec_()
    #endregion
    