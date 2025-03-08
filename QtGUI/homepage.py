from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from ui_homepage import Ui_Form  # Import the UI class

class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()  # Create a central widget
        self.ui = Ui_Form()  # Create an instance of the UI
        self.ui.setupUi(self.central_widget)  # Set up the UI on central_widget
        self.setCentralWidget(self.central_widget)  # Assign the central widget to QMainWindow

if __name__ == "__main__":
    app = QApplication([])
    window = HomePage()
    window.show()
    app.exec()