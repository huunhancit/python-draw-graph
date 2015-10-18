#!/usr/bin/python
# -*- coding: utf-8 -*-
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
import sys
from PyQt4 import QtGui,QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import csv
import random
import os

class Project(QtGui.QWidget):
	def __init__(self):
		super(Project, self).__init__()
		self.pathtemp=""
		self.initUI()
		
    	def initUI(self):
		# tao cac componet
		strname = "Dương Hữu Phước - 1111445"
		strname=strname.decode('utf-8')
		strtitle = "Niên luận mạng máy tính K37"
		strtitle=strtitle.decode('utf-8')
		title = QtGui.QLabel(strtitle)
		title.setText("<font style='color: red;background: white;font-size:20pt'>"+strtitle+"</font>")
		title.setAlignment(Qt.AlignCenter)
		title.setMinimumWidth(200)
		title.setMinimumHeight(50)
		
		name = QtGui.QLabel(strname)
		name.setText("<font style='color: red;background: white;font-size:13pt'>"+strname+"</font>")
		name.setAlignment(Qt.AlignCenter)
		#name.setMinimumWidth(200)
		#name.setMinimumHeight(50)		

		path = QtGui.QLabel('Path: ')
		self.txtpath = QtGui.QLineEdit()
		btnsave = QtGui.QPushButton("Save")
		btnopen = QtGui.QPushButton("Open")
		btndraw = QtGui.QPushButton("Draw")
		btnnew = QtGui.QPushButton("New")
		btncancel = QtGui.QPushButton("Cancel")
		btnsave.setIcon(QtGui.QIcon('save.ico'))
		btnopen.setIcon(QtGui.QIcon('open.ico'))
		btndraw.setIcon(QtGui.QIcon('draw.ico'))
		btnnew.setIcon(QtGui.QIcon('new.ico'))
		btncancel.setIcon(QtGui.QIcon('cancel.ico'))
		btnsave.setFixedHeight(50);
		btnnew.setFixedHeight(50);
		btndraw.setFixedHeight(50);
		btncancel.setFixedHeight(50);

		btnsave.setFixedWidth(150);
		btnnew.setFixedWidth(150);
		btndraw.setFixedWidth(150);
		btncancel.setFixedWidth(150);

		#btnopen.setFixedHeight(50);
		btnopen.setFixedWidth(150);
		# event button
		btnnew.clicked.connect(self.eventNew)
		btnopen.clicked.connect(self.eventOpen)
		btndraw.clicked.connect(self.eventPlot)
		btnsave.clicked.connect(self.eventSave)
		btncancel.clicked.connect(self.eventCancel)
		self.figure = plt.figure()
		self.canvas = FigureCanvas(self.figure)

		self.model = QtGui.QStandardItemModel(self)
		self.tableView = QtGui.QTableView(self)
		self.tableView.setModel(self.model)
		self.tableView.horizontalHeader().setStretchLastSection(True)

		# tao layout
		#layout gom path va text
		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(path)
		hbox.addWidget(self.txtpath)
		hbox.addWidget(btnopen)
	
		#lay chua button va table
		hbox2 = QtGui.QHBoxLayout()

		vbox1 = QtGui.QVBoxLayout()
		vbox1.addWidget(btnnew)
		vbox1.addWidget(btnsave)
		vbox1.addWidget(btndraw)
		vbox1.addWidget(btncancel)
		
		hbox2.addLayout(vbox1)
		hbox2.addWidget(self.tableView)
		# tao 1 cai layout chua tat ca cac layout khac
		vboxbig = QtGui.QVBoxLayout()
		#vboxbig.addStretch(1);
		
		vboxbig.addWidget(title)
		vboxbig.addWidget(name)
		
		vboxbig.addLayout(hbox)
		vboxbig.addLayout(hbox2)
		vboxbig.addWidget(self.canvas)
	
		self.setLayout(vboxbig)    
		self.resize(450,600)
		self.setWindowTitle('Expert Python')   
	
        	self.show()
	def openCSV(self, path):
		with open(path, "rb") as filepath:
			for row in csv.reader(filepath):    
				ds = [
				QtGui.QStandardItem(i) 
				for i in row
				]
		        	self.model.appendRow(ds)
	def eventOpen (self):
		try:
			self.tableView.model().clear()
			path= QtGui.QFileDialog.getOpenFileName(self,'Open file','','CSV(*.csv)')
			self.openCSV(path)
			self.pathtemp=path
			self.txtpath.setText(str(path))
			print self.pathtemp;
		except:
			 QtGui.QMessageBox.information(self, "Open fail","Open fail !")
	def eventNew (self):
		try:
			self.tableView.model().clear()
			self.pathtemp="";
			self.txtpath.setText("")
			self.figure.clear()
			self.canvas.draw()
		except:
			QtGui.QMessageBox.information(self, "New fail","New fail !")

	def eventPlot(self):
		try:
			x = []
			y = []
			#z = []
			fileopen = open(self.pathtemp,'r')
			fe = fileopen.read().split('\n')
			fileopen.close()
			for i in fe:
			    if len(i):
				a,b = i.split(',')
				x.append(int(a))
				y.append(int(b))
				#z.append(int(c))
			ax = self.figure.add_subplot(1,1,1)
			ax.hold(False)
			ax.plot(x,y, '*-')
			self.canvas.draw()
		except:
			QtGui.QMessageBox.information(self, "Draw fail","Draw fail !")
	
	def eventSave(self):
		try:
			with open(self.pathtemp, "wb") as fileout:
		   		ww = csv.writer(fileout)
		    		for i in range(self.model.rowCount()):
		        		truong = [self.model.data(self.model.index(i, j),QtCore.Qt.DisplayRole)    
				    		for j in range(self.model.columnCount())]
		        		ww.writerow(truong)
			QtGui.QMessageBox.information(self, "Save info","Saved !")
		except:
			QtGui.QMessageBox.information(self, "Save info","Not Save !")
	def eventCancel(self):
		reply = QtGui.QMessageBox.question(self, 'Quit',"Are you sure to quit?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

		if reply == QtGui.QMessageBox.Yes:
		    self.close()
		else:
		    pass  

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Project()
    sys.exit(app.exec_())
