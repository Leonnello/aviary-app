from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt, QEvent, pyqtSignal
from PyQt6.QtGui import QPixmap

import re
import os
import shutil

# custom class for clickable Frame
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


class FileObjectFrame(QFrame):
    leftClicked = pyqtSignal()
    
    def __init__(self, file_name, parent=None, orig_color="#81CFE1", hover_color="#AAAAAA"):
        super().__init__(parent)
        
        self.orig_color = orig_color
        self.hover_color = hover_color
        
        self.setMouseTracking(True)
        self.installEventFilter(self)
        
        # Ugly GUI code
        self.leftClicked.connect(lambda: self.on_file_clicked(file_name))
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)
        self.setFixedSize(120, 110)
        self.setStyleSheet("""
                            background-color: #81CFE1;
                            border-radius: 20px;
                            border: 5 solid #81CFE1;
                            """)
        
        # icon
        file_icon = QLabel()
        file_icon.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        file_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        file_icon.setStyleSheet("color: #1A1F71;")
        file_icon.setPixmap(QPixmap("QtGUI/doc_icon.png"))
        
        # label
        file_name_label = QLabel()
        file_name_label.setText(file_name)
        file_name_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Maximum)
        file_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.layout().addWidget(file_icon)
        self.layout().addWidget(file_name_label)
        
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
        style = self.styleSheet()
        
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
        
        self.setStyleSheet(style)
        
    def on_file_clicked(self, file):
            print(f"file clicked: {file}")
            
            # NOTE: insert code to open file here

# custom class to upload files
# NOTE: Need to revise when there's db/storage
class UploadFrame(QFrame):
    fileDropped = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.orig_frame = parent
        
        self.setMouseTracking(True)
        self.orig_frame.setAcceptDrops(True)
        self.orig_frame.installEventFilter(self)  
        
        # Save file to system
        # NOTE: Testing only, temp save to local folder for now
        # Will change to system db or cloud save? later
        self.folder_path = os.path.join(os.getcwd(), 'test_folder')
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

    # capture events, including from children
    def eventFilter(self, obj, event):        
        if event.type() == QEvent.Type.DragEnter:
            if event.mimeData().hasUrls():
                event.acceptProposedAction()
                self.changeColor("#F0F4FF")
                return True
        
        if event.type() == QEvent.Type.DragLeave:
            self.changeColor("#E4EAFE")
            return True
            
        if event.type() == QEvent.Type.DragMove:    
            event.acceptProposedAction()
            return True
            
        if event.type() == QEvent.Type.Drop:    
            files = event.mimeData().urls()
            for file_url in files:
                file_path = file_url.toLocalFile()
                self.upload_file(file_path)
            
            self.changeColor("#E4EAFE")
            return True
        
        return super().eventFilter(obj, event)
            
    # save uploaded file
    # NOTE: Need to revise later when there's db/storage
    # NOTE: wip, testing
    def upload_file(self, file_path):
        file_name = os.path.basename(file_path)
        destination_path = os.path.join(self.folder_path, file_name)
        shutil.copy(file_path, destination_path)
        
        self.fileDropped.emit(file_name)
        
    def changeColor(self, color):
        style = self.orig_frame.styleSheet()
        
        # get old color using regex and replace
        style_color = r"background-color:[^;]+;"  
        new_color = f"background-color: {color};"
        style = re.sub(style_color, new_color, style)
        
        self.orig_frame.setStyleSheet(style)