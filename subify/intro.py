# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'intro.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(563, 412)
        self.cwMain = QtWidgets.QWidget(MainWindow)
        self.cwMain.setObjectName("cwMain")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.cwMain)
        self.verticalLayout.setObjectName("verticalLayout")
        self.hlButtons = QtWidgets.QHBoxLayout()
        self.hlButtons.setObjectName("hlButtons")
        self.btnNewProject = QtWidgets.QPushButton(self.cwMain)
        self.btnNewProject.setObjectName("btnNewProject")
        self.hlButtons.addWidget(self.btnNewProject)
        self.btnOpenProject = QtWidgets.QPushButton(self.cwMain)
        self.btnOpenProject.setObjectName("btnOpenProject")
        self.hlButtons.addWidget(self.btnOpenProject)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hlButtons.addItem(spacerItem)
        self.btnClose = QtWidgets.QPushButton(self.cwMain)
        self.btnClose.setObjectName("btnClose")
        self.hlButtons.addWidget(self.btnClose)
        self.verticalLayout.addLayout(self.hlButtons)
        self.hlLogo = QtWidgets.QHBoxLayout()
        self.hlLogo.setObjectName("hlLogo")
        self.gvLogo = QtWidgets.QGraphicsView(self.cwMain)
        self.gvLogo.setObjectName("gvLogo")
        self.hlLogo.addWidget(self.gvLogo)
        self.verticalLayout.addLayout(self.hlLogo)
        MainWindow.setCentralWidget(self.cwMain)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Subify"))
        self.btnNewProject.setText(_translate("MainWindow", "New Project..."))
        self.btnOpenProject.setText(_translate("MainWindow", "Open Project..."))
        self.btnClose.setText(_translate("MainWindow", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
