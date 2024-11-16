from autotex import Autotex
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QCheckBox, QVBoxLayout, QWidget, QLineEdit, QRadioButton, QHBoxLayout
from sys import argv
from functools import partial


app = QApplication(argv)

class MainApp(QMainWindow):

    def __init__(self, logic:Autotex):
        super().__init__()
        self.setWindowTitle("AutoMats for Source")
        self.mat_name = ""
        self.is_pbr = False
        self.logic = logic
        self.format = ""

        layout = QVBoxLayout()

        widgets = [QLabel("Mettre les textures dans le dossier mats"),
                  QCheckBox("Textures PBR"),
                  'FormatSelection',
                  QLineEdit(),
                  QPushButton("CONVERTIR")
                  ]
        
        format_select = QHBoxLayout()

        radio_buttons = [QRadioButton(name) for name in ["png", "jpg", "jpeg", "tga", "bmp", "dds", "gif"]]

        widgets[1].stateChanged.connect(self.pbr_changed)
        widgets[3].textChanged.connect(self.text_changed)
        widgets[4].clicked.connect(self.button_pressed)


        for button in radio_buttons:
            button.toggled.connect(self.radio_selected)
            format_select.addWidget(button)

        for w in widgets:
            if w == 'FormatSelection':
                layout.addLayout(format_select)
            else:
                layout.addWidget(w)

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

    def text_changed(self, texte):
        self.mat_name = texte

    def button_pressed(self):
        self.logic.convert_to_dtx5_vtf(self.mat_name, self.is_pbr, self.format)

    def pbr_changed(self, state):
        self.is_pbr = state == 2

    def radio_selected(self, state):
        if state:
            self.format = self.sender().text()
logic = Autotex(".//mats//", ".//mats//output")

window = MainApp(logic)
window.show()

app.exec()