# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Sun Mar 24 15:56:24 2013
#      by: PyQt4 UI code generator 4.10
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
        MainWindow.setEnabled(True)
        MainWindow.resize(480, 640)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.icon_layout = QtGui.QHBoxLayout()
        self.icon_layout.setObjectName(_fromUtf8("icon_layout"))
        self.gv_icon = QtGui.QGraphicsView(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gv_icon.sizePolicy().hasHeightForWidth())
        self.gv_icon.setSizePolicy(sizePolicy)
        self.gv_icon.setMaximumSize(QtCore.QSize(76, 76))
        self.gv_icon.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gv_icon.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gv_icon.setObjectName(_fromUtf8("gv_icon"))
        self.icon_layout.addWidget(self.gv_icon)
        self.lb_icon = QtGui.QLabel(self.centralwidget)
        self.lb_icon.setObjectName(_fromUtf8("lb_icon"))
        self.icon_layout.addWidget(self.lb_icon)
        self.verticalLayout.addLayout(self.icon_layout)
        self.canvas_layout = QtGui.QHBoxLayout()
        self.canvas_layout.setObjectName(_fromUtf8("canvas_layout"))
        self.tb_collection = QtGui.QTableWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_collection.sizePolicy().hasHeightForWidth())
        self.tb_collection.setSizePolicy(sizePolicy)
        self.tb_collection.setMinimumSize(QtCore.QSize(76, 0))
        self.tb_collection.setMaximumSize(QtCore.QSize(94, 16777215))
        self.tb_collection.setBaseSize(QtCore.QSize(0, 0))
        self.tb_collection.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tb_collection.setIconSize(QtCore.QSize(76, 76))
        self.tb_collection.setObjectName(_fromUtf8("tb_collection"))
        self.tb_collection.setColumnCount(0)
        self.tb_collection.setRowCount(0)
        self.tb_collection.horizontalHeader().setVisible(False)
        self.tb_collection.horizontalHeader().setDefaultSectionSize(76)
        self.tb_collection.horizontalHeader().setMinimumSectionSize(76)
        self.tb_collection.verticalHeader().setVisible(False)
        self.tb_collection.verticalHeader().setDefaultSectionSize(76)
        self.tb_collection.verticalHeader().setMinimumSectionSize(76)
        self.canvas_layout.addWidget(self.tb_collection)
        self.gv_canvas = QtGui.QGraphicsView(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gv_canvas.sizePolicy().hasHeightForWidth())
        self.gv_canvas.setSizePolicy(sizePolicy)
        self.gv_canvas.setMouseTracking(True)
        self.gv_canvas.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.gv_canvas.setObjectName(_fromUtf8("gv_canvas"))
        self.canvas_layout.addWidget(self.gv_canvas)
        self.verticalLayout.addLayout(self.canvas_layout)
        self.probar = QtGui.QProgressBar(self.centralwidget)
        self.probar.setProperty("value", 24)
        self.probar.setObjectName(_fromUtf8("probar"))
        self.verticalLayout.addWidget(self.probar)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.lb_icon.setText(_translate("MainWindow", "TextLabel", None))
        self.probar.setFormat(_translate("MainWindow", "%p%", None))

