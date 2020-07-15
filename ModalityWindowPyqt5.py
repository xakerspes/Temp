import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal


class MainWindow(QMainWindow):
    """
    //Main window class
    """
    my_signal = pyqtSignal()

    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)

        # Set the title and size of the main window
        self.setWindowTitle('main window')
        self.resize(400, 300)

        # Create button
        self.btn = QPushButton(self)
        self.btn.setText('Pop up dialog')
        self.btn.clicked.connect(self.show_dialog)

        # Custom signal binding
        self.my_signal.connect(self.test)

        # Create dialog object
        self.dialog = Dialog(self)

    def show_dialog(self):
        self.dialog.show()
        self.dialog.exec()

    def test(self):
        self.btn.setText('I changed.')


class Dialog(QDialog):
    """
    //Dialog class
    """
    my_signal = pyqtSignal()

    def __init__(self, parent, *args):
        super(Dialog, self).__init__(*args)

        # Set the title and size of the dialog box
        self.setWindowTitle('Dialog box')
        self.resize(200, 200)
        self.setWindowModality(Qt.ApplicationModal)
        self.btn = QPushButton(self)
        self.btn.setText('Change the name of the main window button')
        self.btn.clicked.connect(self.my_signal.emit)

        # Custom signal binding
        self.my_signal.connect(parent.my_signal.emit)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MainWindow()
    demo.show()
    sys.exit(app.exec())
