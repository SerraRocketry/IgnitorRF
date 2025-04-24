from PySide6.QtCore import (QCoreApplication, QSize, Qt, QMetaObject, QRect)
from PySide6.QtGui import (QPalette, QColor, QFont, QCursor, QTextCursor, QPixmap)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QLabel, QMainWindow,
                               QPushButton, QScrollArea, QWidget, QAbstractScrollArea, QTextEdit)
# open image with PIL
from PIL import Image
import os
from pathlib import Path

# Get the current directory
current_dir = Path(__file__).resolve().parent
# Get the parent directory
parent_dir = current_dir.parent
# Get the path to the image
image_path = os.path.join(parent_dir, 'Assets', 'LOGO.png')
# Check if the image exists
if not os.path.exists(image_path):
    raise FileNotFoundError(f"Image not found: {image_path}")
# Load the image with PIL
image = Image.open(image_path)
# # Resize the image to 181x141
# image = image.resize((181, 181))
# # Save the image
# image.save(image_path)


class Ui_IgnitorRF(object):
    def __init__(self, IgnitorRF, ports: list):
        IgnitorRF.setObjectName("IgnitorRF")
        IgnitorRF.setFixedSize(1280, 720)

        # Set palette
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(36, 31, 49))
        palette.setColor(QPalette.ColorRole.Button, QColor(36, 31, 49))
        palette.setColor(QPalette.ColorRole.Text, QColor(203, 203, 226))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(97, 53, 131))
        IgnitorRF.setPalette(palette)

        # Central widget
        self.centralwidget = QWidget(IgnitorRF)
        self.centralwidget.setObjectName("centralwidget")

        # Menu frame
        self.menu = QFrame(self.centralwidget)
        self.menu.setGeometry(10, 10, 201, 701)
        self.menu.setObjectName("menu")

        self.portsBox = QComboBox(self.menu)
        self.portsBox.setGeometry(10, 10, 181, 31)
        self.portsBox.setObjectName("portsBox")
        self.portsBox.addItems(ports)

        self.connectButton = QPushButton("Conectar", self.menu)
        self.connectButton.setGeometry(10, 90, 181, 31)
        self.connectButton.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor))

        self.disconnectButton = QPushButton("Desconectar", self.menu)
        self.disconnectButton.setGeometry(10, 130, 181, 31)
        self.disconnectButton.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor))
        self.disconnectButton.setEnabled(False)

        self.statusLabel = QLabel("Desconectado", self.menu)
        self.statusLabel.setGeometry(0, 60, 201, 20)
        self.statusLabel.setFont(QFont("JetBrains Mono", 16))
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.commandLabel = QLabel("Comandos", self.menu)
        self.commandLabel.setGeometry(0, 200, 201, 20)
        self.commandLabel.setFont(QFont("JetBrains Mono", 16))
        self.commandLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.countdownButton = QPushButton("Iniciar Contagem", self.menu)
        self.countdownButton.setGeometry(10, 230, 181, 26)
        self.countdownButton.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor))
        self.countdownButton.setEnabled(False)

        self.activateButton = QPushButton("Ativar", self.menu)
        self.activateButton.setGeometry(10, 270, 181, 26)
        self.activateButton.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor))
        self.activateButton.setEnabled(False)

        self.desactivateButton = QPushButton("Desativar", self.menu)
        self.desactivateButton.setGeometry(10, 310, 181, 26)
        self.desactivateButton.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor))
        self.desactivateButton.setEnabled(False)

        self.tareButton = QPushButton("Tare", self.menu)
        self.tareButton.setGeometry(10, 350, 181, 26)
        self.tareButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.tareButton.setEnabled(False)

        self.rebootButton = QPushButton("Reiniciar", self.menu)
        self.rebootButton.setGeometry(10, 390, 181, 26)
        self.rebootButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.rebootButton.setEnabled(False)

        self.closeButton = QPushButton("Fechar", self.menu)
        self.closeButton.setGeometry(10, 655, 181, 31)
        self.closeButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.closeButton.clicked.connect(lambda: self.close_app(IgnitorRF))

        # Show frame
        self.show = QFrame(self.centralwidget)
        self.show.setGeometry(230, 10, 1041, 701)
        self.show.setObjectName("show")

        self.scrollArea = QScrollArea(self.show)
        self.scrollArea.setGeometry(10, 220, 1021, 411)
        self.scrollArea.setFont(QFont("JetBrains Mono"))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        
        self.textEdit = QTextEdit(self.scrollAreaWidgetContents)
        self.textEdit.setGeometry(0, 0, 1021, 411)
        self.textEdit.setFont(QFont("JetBrains Mono", 14))
        self.textEdit.setReadOnly(True)
        self.textCursor = QTextCursor(self.textEdit.document())
        self.textEdit.setTextCursor(self.textCursor)
        block_format = self.textCursor.blockFormat()
        block_format.setTextIndent(50)
        self.textCursor.setBlockFormat(block_format)
        self.textCursor.insertText("Aguardando conexão...\n")
        self.textEdit.textChanged.connect(lambda: self.textEdit.moveCursor(QTextCursor.MoveOperation.End))

        self.receivedLabel = QLabel("Aguardando conexão.", self.show)
        self.receivedLabel.setGeometry(0, 50, 1041, 91)
        self.receivedLabel.setFont(QFont("JetBrains Mono ExtraBold", 32))
        self.receivedLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logButton = QPushButton("Salvar Log", self.show)
        self.logButton.setGeometry(440, 650, 161, 31)
        self.logButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.logButton.setEnabled(False)

        self.pingLabel = QLabel("0.0 ms", self.show)
        self.pingLabel.setGeometry(830, 670, 201, 20)
        self.pingLabel.setFont(QFont("JetBrains Mono", 10))
        self.pingLabel.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Lines
        self.line = QFrame(self.show)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(0, 190, 1041, 31))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.line_2 = QFrame(self.menu)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(0, 160, 201, 51))
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setGeometry(QRect(205, 0, 31, 721))
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.line_4 = QFrame(self.menu)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setGeometry(QRect(0, 610, 201, 51))
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.line_5 = QFrame(self.menu)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setGeometry(QRect(0, 410, 201, 51))
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.logoLabel = QLabel(self.menu)
        self.logoLabel.setGeometry(15, 460, 181, 181)
        self.logoLabel.setPixmap(QPixmap(image_path))
        self.logoLabel.setScaledContents(True)

        IgnitorRF.setCentralWidget(self.centralwidget)

        self.retranslateUi(IgnitorRF)
        QMetaObject.connectSlotsByName(IgnitorRF)

    def retranslateUi(self, IgnitorRF):
        IgnitorRF.setWindowTitle(QCoreApplication.translate(
            "IgnitorRF", "Ignitor RF", None))

    def close_app(self, IgnitorRF):
        IgnitorRF.close()


if __name__ == "__main__":
    app = QApplication([])
    MainWindow = QMainWindow()
    ports = ['COM1', 'COM2', 'COM3']
    ui = Ui_IgnitorRF(IgnitorRF=MainWindow, ports=ports)
    MainWindow.show()
    app.exec()
