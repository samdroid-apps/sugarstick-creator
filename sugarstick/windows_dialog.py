# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data/sugarstick-creator.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(652, 530)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(477, 519))
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(_fromUtf8("background-color: white;"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(477, 519))
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, -1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.label = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setStyleSheet(_fromUtf8(""))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/sugarstick-header.png")))
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_9.addWidget(self.label)
        self.gridLayout.addLayout(self.horizontalLayout_9, 0, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setContentsMargins(9, -1, 9, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.driveBox = QtGui.QComboBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.driveBox.sizePolicy().hasHeightForWidth())
        self.driveBox.setSizePolicy(sizePolicy)
        self.driveBox.setStyleSheet(_fromUtf8("background-color: #808080;\n"
"color: white;\n"
"border-radius: 13px;\n"
"border: 2px solid #2e3436;"))
        self.driveBox.setEditable(False)
        self.driveBox.setInsertPolicy(QtGui.QComboBox.InsertAtTop)
        self.driveBox.setDuplicatesEnabled(False)
        self.driveBox.setObjectName(_fromUtf8("driveBox"))
        self.horizontalLayout.addWidget(self.driveBox)
        self.refreshDevicesButton = QtGui.QPushButton(self.groupBox_2)
        self.refreshDevicesButton.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.refreshDevicesButton.setStyleSheet(_fromUtf8(""))
        self.refreshDevicesButton.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refreshDevicesButton.setIcon(icon)
        self.refreshDevicesButton.setFlat(True)
        self.refreshDevicesButton.setObjectName(_fromUtf8("refreshDevicesButton"))
        self.horizontalLayout.addWidget(self.refreshDevicesButton)
        self.gridLayout_3.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_3.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 2, 1)
        self.horizontalLayout_3.addWidget(self.groupBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.nonDestructiveButton = QtGui.QRadioButton(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nonDestructiveButton.sizePolicy().hasHeightForWidth())
        self.nonDestructiveButton.setSizePolicy(sizePolicy)
        self.nonDestructiveButton.setChecked(True)
        self.nonDestructiveButton.setObjectName(_fromUtf8("nonDestructiveButton"))
        self.gridLayout_2.addWidget(self.nonDestructiveButton, 0, 0, 1, 1)
        self.textEdit = QtGui.QTextEdit(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.textEdit.setFont(font)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout_2.addWidget(self.textEdit, 2, 0, 1, 1)
        self.progressBar = QtGui.QProgressBar(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout_2.addWidget(self.progressBar, 3, 0, 1, 1)
        self.destructiveButton = QtGui.QRadioButton(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.destructiveButton.sizePolicy().hasHeightForWidth())
        self.destructiveButton.setSizePolicy(sizePolicy)
        self.destructiveButton.setObjectName(_fromUtf8("destructiveButton"))
        self.gridLayout_2.addWidget(self.destructiveButton, 1, 0, 1, 1)
        self.startButton = QtGui.QPushButton(self.groupBox_3)
        self.startButton.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startButton.sizePolicy().hasHeightForWidth())
        self.startButton.setSizePolicy(sizePolicy)
        self.startButton.setStyleSheet(_fromUtf8("background-color: #808080;\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 17px;\n"
"    border-color: #2e3436;\n"
"color: white;\n"
"font-weight: bold;\n"
"padding: 5px;"))
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.gridLayout_2.addWidget(self.startButton, 4, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Sugar Stick Creator", None))
        self.groupBox_2.setWhatsThis(_translate("MainWindow", "This is the USB stick that you want to install your Live CD on.  This device must be formatted with the FAT filesystem.", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "USB Stick", None))
        self.label_3.setText(_translate("MainWindow", "Click the button on the right to refresh the list", None))
        self.label_2.setText(_translate("MainWindow", "Plug in a USB Stick with 2GB storage or larger and select it from the list", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Method", None))
        self.nonDestructiveButton.setToolTip(_translate("MainWindow", "This method uses the \'cp\' command to copy the files from the ISO on to your USB key, without deleting any existing files.", None))
        self.nonDestructiveButton.setText(_translate("MainWindow", "Add Sugar Alongside USB Files (cp)", None))
        self.textEdit.setWhatsThis(_translate("MainWindow", "This is the status console, where all messages get written to.", None))
        self.progressBar.setWhatsThis(_translate("MainWindow", "This is the progress bar that will indicate how far along in the LiveUSB creation process you are", None))
        self.destructiveButton.setToolTip(_translate("MainWindow", "This method uses the \'dd\' comand to copy the ISO directly to your USB device, destroying any pre-existing data/partitions. This method tends to be more reliable with regard to booting, especially with UEFI systems. This method also works with DVD images.", None))
        self.destructiveButton.setText(_translate("MainWindow", "Replace USB Files with Sugar (dd)", None))
        self.startButton.setWhatsThis(_translate("MainWindow", "This button will begin the LiveUSB creation process.  This entails optionally downloading a release (if an existing one wasn\'t selected),  extracting the ISO to the USB device, creating the persistent overlay, and installing the bootloader.", None))
        self.startButton.setText(_translate("MainWindow", "Create Sugar on a Stick!", None))

import resources_rc
