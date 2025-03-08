from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QEvent, pyqtSignal

import re

#custom class for clickable Frame
class InteractableFrame(QFrame):
    leftClicked = pyqtSignal()
    
    def __init__(self, parent=None, orig_color="#81CFE1", hover_color="#AAAAAA"):
        super().__init__(parent)
        
        self.orig_frame = parent
        
        self.orig_color = orig_color
        self.hover_color = hover_color
        
        self.setMouseTracking(True)
        self.orig_frame.installEventFilter(self)
        
    # capture events, including from children
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Enter:
            self.changeColor(self.hover_color)
            return True
        
        if event.type() == QEvent.Type.Leave:
            self.changeColor(self.orig_color)
            return True
        
        if event.type() == QEvent.Type.MouseButtonPress:
            self.leftClicked.emit()
            return True
        
        return super().eventFilter(obj, event)
    
    def changeColor(self, color):
        style = self.orig_frame.styleSheet()
        
        # get old color using regex and replace
        style_color = r"background-color:[^;]+;"  
        new_color = f"background-color: {color};"
        style = re.sub(style_color, new_color, style)
        
        # regex for border color
        style_color = r"border:\s*(\d+)\s+([a-zA-Z]+)\s+(#[A-Fa-f0-9]{6});"  
        new_color = rf"border: \g<1> \g<2> {color};"
        
        # only apply if there's a border
        if re.search(style_color, style):
            style = re.sub(style_color, new_color, style)
        
        self.orig_frame.setStyleSheet(style)