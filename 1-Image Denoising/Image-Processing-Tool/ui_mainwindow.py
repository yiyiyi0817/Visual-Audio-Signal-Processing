# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setWindowTitle("Image Processing Tool")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/IPT.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout1 = QtWidgets.QVBoxLayout()
        self.verticalLayout1.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout1.setObjectName("verticalLayout1")
        self.horizontalLayout.addLayout(self.verticalLayout1)
        self.verticalLayout2 = QtWidgets.QVBoxLayout()
        self.verticalLayout2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout2.setObjectName("verticalLayout2")
        self.horizontalLayout.addLayout(self.verticalLayout2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.toolbar = QtWidgets.QToolBar(MainWindow)
        self.toolbar.setWindowTitle("")
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.toolbar.setObjectName("toolbar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setText("Open")
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setText("Save")
        self.actionSave.setObjectName("actionSave")
        self.actionGaussNoise = QtWidgets.QAction(MainWindow)
        self.actionGaussNoise.setText("GaussNoise")
        self.actionGaussNoise.setObjectName("actionGaussNoise")
        self.actionSPNoise = QtWidgets.QAction(MainWindow)
        self.actionSPNoise.setText("SPNoise")
        self.actionSPNoise.setObjectName("actionSPNoise")
        self.actionMedianFilter = QtWidgets.QAction(MainWindow)
        self.actionMedianFilter.setText("MedianFilter")
        self.actionMedianFilter.setObjectName("actionMedianFilter")
        self.actionMeansFilter = QtWidgets.QAction(MainWindow)
        self.actionMeansFilter.setText("MeansFilter")
        self.actionMeansFilter.setObjectName("actionMeansFilter")
        self.actionEqualize = QtWidgets.QAction(MainWindow)
        self.actionEqualize.setText("Equalize")
        self.actionEqualize.setObjectName("Equalize")
        self.actionNormalize = QtWidgets.QAction(MainWindow)
        self.actionNormalize.setText("Normalize")
        self.actionNormalize.setObjectName("actionNormalize")
        self.actionDilate = QtWidgets.QAction(MainWindow)
        self.actionDilate.setText("Dilate")
        self.actionDilate.setObjectName("actionDilate")
        self.actionErode = QtWidgets.QAction(MainWindow)
        self.actionErode.setText("Erode")
        self.actionErode.setObjectName("actionErode")
        self.toolbar.addAction(self.actionOpen)
        self.toolbar.addAction(self.actionSave)
        self.toolbar.addAction(self.actionGaussNoise)
        self.toolbar.addAction(self.actionSPNoise)
        self.toolbar.addAction(self.actionMedianFilter)
        self.toolbar.addAction(self.actionMeansFilter)
        self.toolbar.addAction(self.actionEqualize)
        self.toolbar.addAction(self.actionNormalize)
        self.toolbar.addAction(self.actionDilate)
        self.toolbar.addAction(self.actionErode)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass

