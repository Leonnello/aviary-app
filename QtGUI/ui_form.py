# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QLabel, QSizePolicy,
    QWidget)

class Ui_AviaryAppGUI(object):
    def setupUi(self, AviaryAppGUI):
        if not AviaryAppGUI.objectName():
            AviaryAppGUI.setObjectName(u"AviaryAppGUI")
        AviaryAppGUI.resize(800, 600)
        self.formLayout = QFormLayout(AviaryAppGUI)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(AviaryAppGUI)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)


        self.retranslateUi(AviaryAppGUI)

        QMetaObject.connectSlotsByName(AviaryAppGUI)
    # setupUi

    def retranslateUi(self, AviaryAppGUI):
        AviaryAppGUI.setWindowTitle(QCoreApplication.translate("AviaryAppGUI", u"AviaryAppGUI", None))
        self.label.setText(QCoreApplication.translate("AviaryAppGUI", u"Insert main app ui here", None))
    # retranslateUi

