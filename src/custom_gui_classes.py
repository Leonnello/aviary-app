from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, pyqtSignal

#custom class for clickable Frame
# NOTE: still testing
class InteractableFrame(QFrame):
    # custom signal, testing
    leftClicked = pyqtSignal()
    
    def __init__(self, parent=None, orig_color="#E4EAFE", hover_color="gray"):
        super().__init__(parent)
        
        self.orig_color = orig_color
        self.hover_color = hover_color
        
        self.setMouseTracking(True)  

    def enterEvent(self, event):
        self.setStyleSheet(f"background-color: {self.orig_color};")

    def leaveEvent(self, event):
        self.setStyleSheet(f"background-color: {self.hover_color};")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.leftClicked.emit()
            print("test clicked")