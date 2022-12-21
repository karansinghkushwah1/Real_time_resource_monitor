################################################################################
################################################################################

import sys
import platform
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime,
                          QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase,
                         QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *
from PyQt5 import uic
import psutil
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from pathlib import Path
import numpy as np
from collections import deque
from PyQt5.uic import loadUi
import datetime
from PyQt5.QtWidgets import QDialog, QApplication
import time

# GLOBALS
counter = 0
jumper = 10
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

'''class AnotherWindow(QWidget):
	def __init__(self):
		super().__init__()
		layout = QVBoxLayout()
		self.label = QLabel("Another Window")
		layout.addWidget(self.label)
		self.setLayout(layout)
'''
class ProcessWindow(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("table3.ui",self)
        # self.tableWidget.setColumnWidth(0,250)
        # self.tableWidget.setColumnWidth(1,100)
        self.pushButton.clicked.connect(self.on_click_ref)
        
        self.loaddata()

    def on_click_ref(self):
    	self.loaddata()
    	
    def loaddata(self):
        #Getting application process information using psutil
        people = []
        x = 0
        
        #for process in psutil.process_iter(attrs=None, ad_value=None):
        #    pi = process.as_dict(attrs=['name','cpu_percent'])
        
        #time.sleep(1)
        numProc = 0
        numRunning = 0
        numSleeping = 0
        numThreads = 0
        memoryTot = 0
        
        for process in psutil.process_iter(attrs=None, ad_value=None):
        #for process in psutil.process_iter():
            pi = process.as_dict(attrs=['name','cpu_percent'])
            dic = {}
            #print(pi)
            dic["PID"] = str(process.pid)
            
            # pids.append(process.pid)
            #print("1")
            
            #dic["Process Name"] = str(process.name())
            
            #
            #print("2")
            
            #dic["CPU%"] = str(process.cpu_percent(interval=1)/psutil.cpu_count())
            
            dic["Process Name"] = str(pi['name'])
            #dic["CPU%"] = str(pi['cpu_percent']/psutil.cpu_count())
            
            #print("3")
            # cpu_usage.append(process.cpu_percent(interval=1)/psutil.cpu_count())

            dic["Memory (MB)"] = str(round(process.memory_info().rss/(1024*1024),2))
            # memory_usage.append(round(process.memory_info().rss/(1024*1024),2))

            dic["Memory%"] = str(round(process.memory_percent(),2))
            # memory_usage_percentage.append(round(process.memory_percent(),2))

            dic["Status"] = str(process.status())
            
            if(dic["Status"] == "sleeping"):
            	numSleeping = numSleeping + 1
            elif(dic["Status"] == "running"):
            	numRunning = numRunning + 1
            	
            
            	

            dic["Created Time"] = str(datetime.datetime.fromtimestamp(process.create_time()).strftime("%Y%m%d - %H:%M:%S"))
            # create_time.append(datetime.datetime.fromtimestamp(
            #                     process.create_time()).strftime("%Y%m%d - %H:%M:%S"))
            # status.append(process.status())

            dic["Threads"] = str(process.num_threads())
            
            numThreads = numThreads + int(dic["Threads"])
            memoryTot = memoryTot + float(dic["Memory (MB)"])
            # threads.append(process.num_threads())
            people.append(dic)
            numProc = numProc + 1
            ##x = x+1
            ##if(x == 3):
            ##	break
        
        
        # people=[{"PID":"1","Process Name":"process1","CPU%":"95", "Memory (MB)":"45", "Memory%":"34", "Status":"Sleeping", "Created Time":"12", "Threads":"34"}, {"PID":"2","Process Name":"process1","CPU%":"95", "Memory (MB)":"45", "Memory%":"34", "Status":"Sleeping", "Created Time":"12", "Threads":"34"},
        #         {"PID":"5","Process Name":"process1","CPU%":"95", "Memory (MB)":"45", "Memory%":"34", "Status":"Sleeping", "Created Time":"12", "Threads":"34"}]
        row=0
        self.tableWidget.setRowCount(len(people))
        for person in people:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(person["PID"]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(person["Process Name"]))
            #self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(person["CPU%"]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(person["Memory (MB)"]))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(person["Memory%"]))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(person["Status"]))
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(person["Created Time"]))
            self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(person["Threads"]))
            row=row+1	
            
        self.label_3.setText(str(numProc))
        self.label_6.setText(str(numRunning))
        self.label_8.setText(str(numSleeping))
        self.label_4.setText(str(numThreads))
        self.label_11.setText(str(memoryTot))
        
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)
        self.updnet = False
        self.prevSent = 0
        self.prevRec = 0
        self.ui = uic.loadUi("main3.ui", self)
        self.ui.label_8.setStyleSheet('.QLabel {font-size: 20pt; color: white; }')
        self.cpu_percent = 0
        self.ram_percent = 0
        self.traces = dict()
        self.timestamp = 0
        self.timeaxis = []
        self.cpuaxis = []
        self.ramaxis = []
        # self.csv_file = open(datafile, 'w')
        # self.csv_writer = csv.writer(self.csv_file, delimiter=',')
        self.current_timer_graph = None
        self.graph_lim = 15
        self.deque_timestamp = deque([], maxlen=self.graph_lim+20)
        self.deque_cpu = deque([], maxlen=self.graph_lim+20)
        self.deque_ram = deque([], maxlen=self.graph_lim+20)
        self.ui.label.setText(
            f"{platform.system()} {platform.machine()}")
        self.ui.label_2.setText(
            f"Processor: {platform.processor()}")

        self.graphwidget1 = PlotWidget(title="CPU percent")
        x1_axis = self.graphwidget1.getAxis('bottom')
        x1_axis.setLabel(text='Time since start (s)')
        y1_axis = self.graphwidget1.getAxis('left')
        y1_axis.setLabel(text='Percent')

        self.graphwidget2 = PlotWidget(title="RAM percent")
        x2_axis = self.graphwidget2.getAxis('bottom')
        x2_axis.setLabel(text='Time since start (s)')
        y2_axis = self.graphwidget2.getAxis('left')
        y2_axis.setLabel(text='Percent')

        self.pushButton.clicked.connect(self.show_cpu_graph)
        self.pushButton_2.clicked.connect(self.show_ram_graph)
        self.pushButton_3.clicked.connect(self.on_click)
        
        
        self.ui.gridLayout.addWidget(self.graphwidget1, 0, 0, 1, 3)
        self.ui.gridLayout.addWidget(self.graphwidget2, 0, 0, 1, 3)

        self.current_timer_systemStat = QtCore.QTimer()
        self.current_timer_systemStat.timeout.connect(
            self.getsystemStatpercent)
        self.current_timer_systemStat.start(1000)
        self.show_cpu_graph()

	
  
    def on_click(self):
        self.w = ProcessWindow()
        self.w.show()
        #print(psutil._ppid_map())
        #print(str(len(psutil.pids()))+" are the number of running processes")
        
    def getsystemStatpercent(self):
        # gives a single float value
        self.cpu_percent = psutil.cpu_percent()
        self.ram_percent = psutil.virtual_memory().percent
        #print(self.ram_percent)
        if(self.ram_percent > 95):
        	print("\a")
        batteryPercent = psutil.sensors_battery().percent
        self.ui.progressBar_2.setValue((int)(batteryPercent))
        self.ui.label_12.setText(str(batteryPercent) + " %")
        net = psutil.net_io_counters(pernic=True)
            
        if(self.updnet == False):
            self.prevSent = net['lo'].bytes_sent
            self.prevRec = net['lo'].bytes_recv
        else:
            nSent = net['lo'].bytes_sent
            nRec = net['lo'].bytes_recv
            
            diffSent = nSent - self.prevSent
            diffRec = nRec - self.prevRec
            
            self.ui.label_8.setText(str(diffSent)+" KB/sec")
            #self.ui.label_9.setText(str(diffRec)+" KB/sec")
        	
            self.prevSent = nSent
            self.prevRec = nRec
            
            
        self.updnet =  not self.updnet
            
        
        #packetsSent = net['lo'].packets_sent
        
        #packetsReceived = net['lo'].packets_recv
        
        #print(sent)
        
       
        #self.ui.label_10.setText(str(packetsSent))
        
        #self.ui.label_11.setText(str(packetsReceived))
        
        self.setValue(self.cpu_percent, self.ui.labelPercentageCPU,
                      self.ui.circularProgressCPU, "rgba(85, 170, 255, 255)")
        self.setValue(self.ram_percent, self.ui.labelPercentageRAM,
                      self.ui.circularProgressRAM, "rgba(30, 194, 192, 1)")

    def start_cpu_graph(self):
        # self.timeaxis = []
        # self.cpuaxis = []
        if self.current_timer_graph:
            self.current_timer_graph.stop()
            self.current_timer_graph.deleteLater()
            self.current_timer_graph = None
        self.current_timer_graph = QtCore.QTimer()
        self.current_timer_graph.timeout.connect(self.update_cpu)
        self.current_timer_graph.start(1000)

    def update_cpu(self):
        self.timestamp += 1

        self.deque_timestamp.append(self.timestamp)
        self.deque_cpu.append(self.cpu_percent)
        self.deque_ram.append(self.ram_percent)
        timeaxis_list = list(self.deque_timestamp)
        cpu_list = list(self.deque_cpu)

        if self.timestamp > self.graph_lim:
            self.graphwidget1.setRange(xRange=[self.timestamp-self.graph_lim+1, self.timestamp], yRange=[
                                       min(cpu_list[-self.graph_lim:]), max(cpu_list[-self.graph_lim:])])
        self.set_plotdata(name="cpu", data_x=timeaxis_list,
                          data_y=cpu_list)

    def start_ram_graph(self):

        if self.current_timer_graph:
            self.current_timer_graph.stop()
            self.current_timer_graph.deleteLater()
            self.current_timer_graph = None
        self.current_timer_graph = QtCore.QTimer()
        self.current_timer_graph.timeout.connect(self.update_ram)
        self.current_timer_graph.start(1000)

    def update_ram(self):
        self.timestamp += 1

        self.deque_timestamp.append(self.timestamp)
        self.deque_cpu.append(self.cpu_percent)
        self.deque_ram.append(self.ram_percent)
        timeaxis_list = list(self.deque_timestamp)
        ram_list = list(self.deque_ram)

        if self.timestamp > self.graph_lim:
            self.graphwidget2.setRange(xRange=[self.timestamp-self.graph_lim+1, self.timestamp], yRange=[
                                       min(ram_list[-self.graph_lim:]), max(ram_list[-self.graph_lim:])])
        self.set_plotdata(name="ram", data_x=timeaxis_list,
                          data_y=ram_list)

    def show_cpu_graph(self):
        self.graphwidget2.hide()
        self.graphwidget1.show()
        self.start_cpu_graph()
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(True)
        self.pushButton.setStyleSheet(
            "QPushButton" "{" "background-color : lightblue;" "}"
        )
        self.pushButton_2.setStyleSheet(
            "QPushButton"
            "{"
            "background-color : rgb(142, 86, 185);"
            "}"
            "QPushButton"
            "{"
            "color : white;"
            "}"
        )

    def show_ram_graph(self):
        self.graphwidget1.hide()
        self.graphwidget2.show()
        # self.graphwidget2.autoRange()
        self.start_ram_graph()
        self.pushButton_2.setEnabled(False)
        self.pushButton.setEnabled(True)
        self.pushButton_2.setStyleSheet(
            "QPushButton" "{" "background-color : lightblue;" "}"
        )
        self.pushButton.setStyleSheet(
            "QPushButton"
            "{"
            "background-color : rgb(142, 86, 185);"
            "}"
            "QPushButton"
            "{"
            "color : white;"
            "}"
        )

    def set_plotdata(self, name, data_x, data_y):
        # print('set_data')
        if name in self.traces:
            self.traces[name].setData(data_x, data_y)
        else:
            if name == "cpu":
                self.traces[name] = self.graphwidget1.getPlotItem().plot(
                    pen=pg.mkPen((85, 170, 255), width=3))

            elif name == "ram":
                self.traces[name] = self.graphwidget2.getPlotItem().plot(
                    pen=pg.mkPen((255, 0, 127), width=3))

    # ==> SET VALUES TO DEF progressBarValue

    def setValue(self, value, labelPercentage, progressBarName, color):

        sliderValue = value

        # HTML TEXT PERCENTAGE
        htmlText = """<p align="center"><span style=" font-size:50pt;">{VALUE}</span><span style=" font-size:40pt; vertical-align:super;">%</span></p>"""
        labelPercentage.setText(htmlText.replace(
            "{VALUE}", f"{sliderValue:.1f}"))

        # CALL DEF progressBarValue
        self.progressBarValue(sliderValue, progressBarName, color)

    # DEF PROGRESS BAR VALUE
    ########################################################################

    def progressBarValue(self, value, widget, color):

        # PROGRESSBAR STYLESHEET BASE
        styleSheet = """
        QFrame{
        	border-radius: 110px;
        	background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 0, 127, 0), stop:{STOP_2} {COLOR});
        }
        """

        # GET PROGRESS BAR VALUE, CONVERT TO FLOAT AND INVERT VALUES
        # stop works of 1.000 to 0.000
        progress = (100 - value) / 100.0

        # GET NEW VALUES
        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)

        # FIX MAX VALUE
        if value == 100:
            stop_1 = "1.000"
            stop_2 = "1.000"

        # SET VALUES TO NEW STYLESHEET
        newStylesheet = styleSheet.replace("{STOP_1}", stop_1).replace(
            "{STOP_2}", stop_2).replace("{COLOR}", color)

        # APPLY STYLESHEET WITH NEW VALUES
        widget.setStyleSheet(newStylesheet)


# ==> SPLASHSCREEN WINDOW
class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # self.ui = Ui_SplashScreen()
        # self.ui.setupUi(self)
       
        ##self.ui = uic.loadUi("splash_screen.ui", self)
       
        # ==> SET INITIAL PROGRESS BAR TO (0) ZERO
        
        ##self.progressBarValue(0)

        # ==> REMOVE STANDARD TITLE BAR
        
        ##self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Remove title bar
        
        # Set background to transparent
        
        ##self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # ==> APPLY DROP SHADOW EFFECT
        
        """self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.ui.circularBg.setGraphicsEffect(self.shadow)
	"""
        # QTIMER ==> START
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        
        # TIMER IN MILLISECONDS
        
        self.timer.start(15)

        # SHOW ==> MAIN WINDOW
        ########################################################################
        
        self.show()
        
        ## ==> END ##

    # DEF TO LOANDING
    ########################################################################
    def progress(self):
        global counter
        global jumper
        value = counter

        # HTML TEXT PERCENTAGE
        
        ##htmlText = """<p><span style=" font-size:68pt;">{VALUE}</span><span style=" font-size:58pt; vertical-align:super;">%</span></p>"""

        # REPLACE VALUE
        
        ##newHtml = htmlText.replace("{VALUE}", str(jumper))

        if(value > jumper):
            # APPLY NEW PERCENTAGE TEXT
            ##self.ui.labelPercentage.setText(newHtml)
            jumper += 10

        # SET VALUE TO PROGRESS BAR
        # fix max value error if > than 100
        if value >= 100:
            value = 1.000
        
        ##self.progressBarValue(value)
        if counter == 10:
            self.main = MainWindow()

        # CLOSE SPLASH SCREE AND OPEN APP
        if counter > 100:
            # STOP TIMER
            self.timer.stop()

            # SHOW MAIN WINDOW
            # self.main = MainWindow()
            self.main.show()

            # CLOSE SPLASH SCREEN
            self.close()

        # INCREASE COUNTER
        counter += 0.5

    # DEF PROGRESS BAR VALUE
    ########################################################################
    def progressBarValue(self, value):

        # PROGRESSBAR STYLESHEET BASE
        styleSheet = """
        QFrame{
        	border-radius: 150px;
        	background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 0, 127, 0), stop:{STOP_2} rgba(85, 170, 255, 255));
        }
        """

        # GET PROGRESS BAR VALUE, CONVERT TO FLOAT AND INVERT VALUES
        # stop works of 1.000 to 0.000
        progress = (100 - value) / 100.0

        # GET NEW VALUES
        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)

        # SET VALUES TO NEW STYLESHEET
        newStylesheet = styleSheet.replace(
            "{STOP_1}", stop_1).replace("{STOP_2}", stop_2)

        # APPLY STYLESHEET WITH NEW VALUES
        self.ui.circularProgress.setStyleSheet(newStylesheet)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())
