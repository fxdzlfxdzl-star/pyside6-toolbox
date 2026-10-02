# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_GreeterWindow(object):
    def setupUi(self, GreeterWindow):
        if not GreeterWindow.objectName():
            GreeterWindow.setObjectName(u"GreeterWindow")
        GreeterWindow.resize(460, 240)
        self.rootLayout = QVBoxLayout(GreeterWindow)
        self.rootLayout.setObjectName(u"rootLayout")
        self.titleLabel = QLabel(GreeterWindow)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setWordWrap(True)

        self.rootLayout.addWidget(self.titleLabel)

        self.inputRow = QHBoxLayout()
        self.inputRow.setObjectName(u"inputRow")
        self.promptLabel = QLabel(GreeterWindow)
        self.promptLabel.setObjectName(u"promptLabel")

        self.inputRow.addWidget(self.promptLabel)

        self.nameEdit = QLineEdit(GreeterWindow)
        self.nameEdit.setObjectName(u"nameEdit")

        self.inputRow.addWidget(self.nameEdit)


        self.rootLayout.addLayout(self.inputRow)

        self.greetButton = QPushButton(GreeterWindow)
        self.greetButton.setObjectName(u"greetButton")

        self.rootLayout.addWidget(self.greetButton)

        self.outputLabel = QLabel(GreeterWindow)
        self.outputLabel.setObjectName(u"outputLabel")
        self.outputLabel.setWordWrap(True)

        self.rootLayout.addWidget(self.outputLabel)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rootLayout.addItem(self.verticalSpacer)


        self.retranslateUi(GreeterWindow)

        QMetaObject.connectSlotsByName(GreeterWindow)
    # setupUi

    def retranslateUi(self, GreeterWindow):
        GreeterWindow.setWindowTitle(QCoreApplication.translate("GreeterWindow", u"Designer \u6d41\u7a0b\u6f14\u793a \u00b7 \u53ef\u5728 pyside6-designer \u91cc\u76f4\u63a5\u6539", None))
        self.titleLabel.setText(QCoreApplication.translate("GreeterWindow", u"\u7528 pyside6-designer \u6253\u5f00\u8fd9\u4e2a .ui\uff0c\u6539\u5b8c\u91cd\u65b0\u7f16\u8bd1\u5373\u53ef", None))
        self.promptLabel.setText(QCoreApplication.translate("GreeterWindow", u"\u6635\u79f0\uff1a", None))
        self.nameEdit.setPlaceholderText(QCoreApplication.translate("GreeterWindow", u"\u8f93\u5165\u70b9\u4ec0\u4e48\u2026\u2026", None))
        self.greetButton.setText(QCoreApplication.translate("GreeterWindow", u"\u6253\u62db\u547c", None))
        self.outputLabel.setText(QCoreApplication.translate("GreeterWindow", u"\uff08\u7ed3\u679c\u4f1a\u663e\u793a\u5728\u8fd9\u91cc\uff09", None))
    # retranslateUi

