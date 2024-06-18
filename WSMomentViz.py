import sys
import matplotlib
import pandas as pd
matplotlib.use('QtAgg')
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.widgets as mwidgets
import time


csv = './WorldSeriesMain.csv'
WSDF = pd.read_csv(csv, index_col=0)
currWSDF = WSDF

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=150, height=150, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


class NarrativeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Story Mode")

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)



        self.layout = QGridLayout()
        self.selectWS = QComboBox()
        self.selectWS.addItem("2023 - Texas Rangers vs Arizona Diamondbacks")
        self.selectWS.addItem("2022 - Houston Astros vs Philadelphia Phillies")
        self.selectWS.addItem("2021 - Atlanta Braves vs Houston Astros")
        self.selectWS.addItem("2020 - Los Angeles Dodgers vs Tampa Bay Rays")
        self.selectWS.addItem("2019 - Washington Nationals vs Houston Astros")
        self.selectWS.addItem("2018 - Boston Red Sox vs Los Angeles Dodgers")
        self.selectWS.addItem("2017 - Houston Astros vs Los Angeles Dodgers")
        self.selectWS.addItem("2016 - Chicago Cubs vs Cleveland Indians")
        self.selectWS.addItem("2015 - Kansas City Royals vs New York Mets")
        self.selectWS.addItem("2014 - San Francisco Giants vs Kansas City Royals")
        self.selectWS.addItem("2013 - Boston Red Sox vs St. Louis Cardinals")
        self.selectWS.addItem("2012 - San Francisco Giants vs Detroit Tigers")
        self.selectWS.addItem("2011 - St. Louis Cardinals vs Texas Rangers")
        self.selectWS.addItem("2010 - San Francisco Giants vs Texas Rangers")
        self.selectWS.addItem("2009 - New York Yankees vs Philadelphia Phillies")
        self.selectWS.addItem("2008 - Philadelphia Phillies vs Tampa Bay Rays")
        self.selectWS.addItem("2007 - Boston Red Sox vs Colorado Rockies")
        self.selectWS.addItem("2006 - St. Louis Cardinals vs Detroit Tigers")
        self.selectWS.addItem("2005 - Chicago White Sox vs Houston Astros")
        self.selectWS.addItem("2004 - Boston Red Sox vs St. Louis Cardinals")
        self.selectWS.addItem("2003 - Florida Marlins vs New York Yankees")
        self.selectWS.addItem("2002 - Anaheim Angels vs San Francisco Giants")
        self.layout.addWidget(self.selectWS, 0, 0)
        self.layout.addWidget(self.buttonBox, 0, 1)

        self.setLayout(self.layout)

class PointDialog(QDialog):
    def __init__(self, points, isNeighbor=False, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("More Play Info")
        myRow = points
        if not isNeighbor:
            for index, row in WSDF.iterrows():
                        if ((row[parent.dropdown1.currentText()] == points[0]) and (row[parent.dropdown2.currentText()] == points[1])):
                            myRow = row
                            break
        

        QBtn = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.layout = QVBoxLayout()

        if not isNeighbor:
            message = QLabel("Play: {}\nYear: {}\nGame: {}\nInning:{}\n\
    Outs: {}\nBases: {}\nScore: {}\nPitchSeq: {}\n\
            \nLeverage: {}\nWin Probability Added: {:.1%}\nRuns Expected Before At-Bat: {}\
            Runs Expectancy Difference After Play: {}".format(myRow['Play'], myRow['Year'], myRow['Game'], myRow['Inning'], myRow['Outs'], myRow['Bases'],
                                                                    myRow['Score'], myRow['PitchSeq'], myRow['LI'], myRow['WPA'], myRow['RE'], myRow['RE24']))
        else:
            message = QLabel("Neighbor: \n{}".format(myRow['Play']))
        
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Filter")

        QBtn = QDialogButtonBox.StandardButton.Reset | QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.StandardButton.Reset).clicked.connect(self.reset)



        self.layout = QGridLayout()
        self.message1 = QLabel("Year")
        message2 = QLabel("Game")
        message3 = QLabel("Inning")
        message4 = QLabel("Event")
        self.layout.addWidget(self.message1, 0, 0)
        self.layout.addWidget(message2, 0, 1)
        self.layout.addWidget(message3, 0, 2)
        self.layout.addWidget(message4, 0, 3)
        self.layout.addWidget(self.buttonBox, 0, 4)


        self.yearWipeButton = QPushButton("Uncheck All")
        self.gameWipeButton = QPushButton("Uncheck All")
        self.inningWipeButton = QPushButton("Uncheck All")
        self.eventWipeButton = QPushButton("Uncheck All")

        self.yearWipeButton.clicked.connect(self.wipe_checks1)
        self.gameWipeButton.clicked.connect(self.wipe_checks2)
        self.inningWipeButton.clicked.connect(self.wipe_checks3)
        self.eventWipeButton.clicked.connect(self.wipe_checks4)


        self.layout.addWidget(self.yearWipeButton, 1, 0)
        self.layout.addWidget(self.gameWipeButton, 1, 1)
        self.layout.addWidget(self.inningWipeButton, 1, 2)
        self.layout.addWidget(self.eventWipeButton, 1, 3)

        #self.layout.addWidget(self.checklist)
        self.yearCheckBox = ['2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002']
        self.gameCheckBox=['Game 1', 'Game 2', 'Game 3', 'Game 4', 'Game 5', 'Game 6', 'Game 7']
        self.InningCheckBox=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13+']
        self.eventCheckBox=['Single', 'Double', 'Triple', 'Home Run', 'Walk', 'Strikeout', 'Stolen Base', 'Other']

        for i, v in enumerate(self.yearCheckBox):
            self.yearCheckBox[i] = QCheckBox(v)
            self.yearCheckBox[i].setCheckState(Qt.CheckState.Checked)
            self.layout.addWidget(self.yearCheckBox[i], 2+i, 0)

        for i, v in enumerate(self.gameCheckBox):
            self.gameCheckBox[i] = QCheckBox(v)
            self.gameCheckBox[i].setCheckState(Qt.CheckState.Checked)
            self.layout.addWidget(self.gameCheckBox[i], 2+i, 1)
        
        for i, v in enumerate(self.InningCheckBox):
            self.InningCheckBox[i] = QCheckBox(v)
            self.InningCheckBox[i].setCheckState(Qt.CheckState.Checked)
            self.layout.addWidget(self.InningCheckBox[i], 2+i, 2)

        for i, v in enumerate(self.eventCheckBox):
            self.eventCheckBox[i] = QCheckBox(v)
            self.eventCheckBox[i].setCheckState(Qt.CheckState.Checked)
            self.layout.addWidget(self.eventCheckBox[i], 2+i, 3)

        self.setLayout(self.layout)
        #parent is a MainWindow calling this
    
    def wipe_checks1(self):
        for i, v in enumerate(self.yearCheckBox):
            self.yearCheckBox[i].setCheckState(Qt.CheckState.Unchecked)

    def wipe_checks2(self):
        for i, v in enumerate(self.gameCheckBox):
            self.gameCheckBox[i].setCheckState(Qt.CheckState.Unchecked)

    def wipe_checks3(self):
        for i, v in enumerate(self.InningCheckBox):
            self.InningCheckBox[i].setCheckState(Qt.CheckState.Unchecked)

    def wipe_checks4(self):
        for i, v in enumerate(self.eventCheckBox):
            self.eventCheckBox[i].setCheckState(Qt.CheckState.Unchecked)



    def reset(self):
        for i in range(0, len(self.yearCheckBox)):
            self.yearCheckBox[i].setCheckState(Qt.CheckState.Checked)

        for i in range(0, len(self.gameCheckBox)):
            self.gameCheckBox[i].setCheckState(Qt.CheckState.Checked)
            
        for i in range(0, len(self.InningCheckBox)):
            self.InningCheckBox[i].setCheckState(Qt.CheckState.Checked)

        for i in range(0, len(self.eventCheckBox)):
            self.eventCheckBox[i].setCheckState(Qt.CheckState.Checked)



class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.

        self.press=False  #for cursor connects
        self.move = False

        self.storyPoints = []
        self.storyDF = None
        self.game = 1
        self.games = []
        self.myCMAP = matplotlib.cm.RdBu_r
        self.storyMode = False
        self.myPoint = 0

        self.sc = MplCanvas(self, width=150, height=150, dpi=100)
        self.myPoints = self.sc.axes.scatter(WSDF['WPA'], WSDF['LI'], alpha=.5, c=WSDF['InningNum'])#, s=WSDF['population']/1000000, alpha=.5, c=WSDF['life_expectancy'])
        self.setCentralWidget(self.sc)
        self.sc.axes.set_xlabel('WPA')
        self.sc.axes.set_ylabel('LI')

        self.sc2 = MplCanvas(self, width=150, height=150, dpi=100)
        self.sc2.axes.scatter(WSDF['RE'], WSDF['RE24'], alpha = .5, c=WSDF['InningNum'])#, s=WSDF['population']/1000000, alpha=.5, c=WSDF['life_expectancy'])
        self.sc2.axes.set_xlabel('RE')
        self.sc2.axes.set_ylabel('RE24')
        self.setWindowTitle("World Series Visualization")

        self.sc3 = MplCanvas(self, width=150, height=150, dpi=100)

        #rectangle stuff
        def onselect(eclick , erelease):
            print(eclick.xdata, eclick.ydata)
            print(erelease.xdata, erelease.ydata)
        rect = mwidgets.RectangleSelector(self.sc.axes, onselect)
        rect.add_state('square')

        xyColumns = ['LI', 'WPA', 'RE', 'RE24']
 
        self.dropdown1 = QComboBox(self)
        for colName in xyColumns:
            self.dropdown1.addItem(colName)
        self.dropdown1.setCurrentText("WPA")
        self.dropdown1.currentTextChanged.connect(self.update_graph)
        xlabel = QLabel("x-axis", self)

        self.dropdown2 = QComboBox(self)
        for colName in xyColumns:
            self.dropdown2.addItem(colName)
        ylabel = QLabel("y-axis", self)
        self.dropdown2.setCurrentText("LI")
        self.dropdown2.currentTextChanged.connect(self.update_graph)

        self.dropdown3 = QComboBox(self)
        clabel = QLabel("Color", self)
        self.dropdown3.addItem("InningNum")
        self.dropdown3.addItem("Outs")
        for colName in xyColumns:
           self.dropdown3.addItem(colName)
        self.dropdown3.setCurrentText("InningNum")
        self.dropdown3.currentTextChanged.connect(self.update_graph)

        self.filterButton1 = QPushButton("Filter", self)
        self.filterButton1.clicked.connect(self.filterGraph1)

        self.graph2Button = QPushButton("Reveal Extra Graph", self)
        self.graph2Button.clicked.connect(self.graph2visibility)

        self.narrative = QPushButton("Story Mode", self)
        


        #2
        self.dropdown12 = QComboBox(self)
        for colName in xyColumns:
           self.dropdown12.addItem(colName)
        self.dropdown12.setCurrentText("RE")
        self.dropdown12.currentTextChanged.connect(self.update_graph2)
        xlabel2 = QLabel("x-axis", self)
        xlabel2#.hide()
        self.dropdown12#.hide()

        self.dropdown22 = QComboBox(self)
        for colName in xyColumns:
           self.dropdown22.addItem(colName)
        ylabel2 = QLabel("y-axis", self)
        ylabel2#.hide()
        self.dropdown22.setCurrentText("RE24")
        self.dropdown22.currentTextChanged.connect(self.update_graph2)
        self.dropdown22#.hide()

        self.dropdown32 = QComboBox(self)
        for colName in xyColumns:
             self.dropdown32.addItem(colName)
        rlabel2 = QLabel("color", self)
        self.dropdown32.addItem("InningNum")
        self.dropdown32.addItem("Outs")
        self.dropdown32.setCurrentText("InningNum")
        self.dropdown32.currentTextChanged.connect(self.update_graph2)
        self.dropdown32#.hide()

        toolbar = NavigationToolbar(self.sc, self)
        toolbar2 = NavigationToolbar(self.sc2, self)
        #toolbar.press_zoom
        #layouts
        self.layout = QtWidgets.QGridLayout()

        self.firstFrame = QtWidgets.QFrame()
        self.secondFrame = QtWidgets.QFrame()
        self.thirdFrame = QtWidgets.QFrame()
        self.layout1 = QtWidgets.QVBoxLayout()
        self.layout2 = QtWidgets.QVBoxLayout()
        self.layout3 = QtWidgets.QVBoxLayout()
        self.firstFrame.setLayout(self.layout1)
        self.secondFrame.setLayout(self.layout2)
        self.thirdFrame.setLayout(self.layout3)

        self.layout1.addWidget(toolbar)
        self.layout2.addWidget(toolbar2)
        self.layout1.addWidget(self.sc)
        self.layout2.addWidget(self.sc2)
        self.layout3.addWidget(self.sc3) #change to sc3

        #self.slider = QtWidgets.QSlider( Qt.Orientation.Horizontal, self.sc)
        #self.slider.setGeometry(QtCore.QRect(500, 300, 1600, 160000))
        #self.slider.setSliderPosition(50)
        #self.slider.setMinimum(1)
        #self.slider2 = QtWidgets.QSlider( Qt.Orientation.Horizontal, self.sc2)
        #self.slider2.setGeometry(QtCore.QRect(500, 300, 1600, 160000))
        #self.slider2.setSliderPosition(50)
        #self.slider2.setMinimum(1)
        #self.layout1.addWidget(self.slider)

        self.layout1.addWidget(xlabel)
        self.layout1.addWidget(self.dropdown1)
        self.layout1.addWidget(ylabel)
        self.layout1.addWidget(self.dropdown2)
        self.layout1.addWidget(clabel)
        self.layout1.addWidget(self.dropdown3)
        self.layout1.addWidget(self.graph2Button)
        self.layout1.addWidget(self.filterButton1)
        self.layout1.addWidget(self.narrative)

        #self.layout2.addWidget(self.slider2)
        self.layout2.addWidget(xlabel2)
        self.layout2.addWidget(self.dropdown12)
        self.layout2.addWidget(ylabel2)
        self.layout2.addWidget(self.dropdown22)
        self.layout2.addWidget(rlabel2)
        self.layout2.addWidget(self.dropdown32)

        self.layout.addWidget(self.firstFrame, 0, 0, 12, 1)
        self.layout.addWidget(self.secondFrame, 0, 1, 9, 1)
        self.layout.addWidget(self.thirdFrame, 0, 2, 9, 1)
        self.firstFrame.show()
        self.secondFrame.hide()
        self.thirdFrame.hide()        
  
        # After each value change, slot "scaletext" will get invoked.
        #self.slider.valueChanged.connect(self.scaleArea)
        #self.slider2.valueChanged.connect(self.scaleArea2)
        

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        self.sc.fig.set_tight_layout('tight')
        self.sc2.fig.set_tight_layout('tight')
        self.sc3.fig.set_tight_layout('tight')




                #Airports annotation display on hover
        self.annot = self.sc.axes.annotate("", xy=(1, 4), xytext=(0.0125, 0.975),
            textcoords='axes fraction',
                            bbox=dict(boxstyle="round", fc="w"), annotation_clip=True,
                            arrowprops=dict(arrowstyle="->"), fontsize='medium', horizontalalignment='left', verticalalignment='top')
        self.annot.set_visible(False)

        self.annot2 = self.sc2.axes.annotate("", xy=(1, 4), xytext=(0.0125, 0.975),
            textcoords='axes fraction',
                            bbox=dict(boxstyle="round", fc="w"), annotation_clip=True,
                            arrowprops=dict(arrowstyle="->"), fontsize = 'small', horizontalalignment='left', verticalalignment='top')
        self.annot2.set_visible(False)

        self.annot3 = self.sc3.axes.annotate("", xy=(1, 4), xytext=(0.0125, 0.975),
            textcoords='axes fraction',
                            bbox=dict(boxstyle="round", fc="w"), annotation_clip=True,
                            arrowprops=dict(arrowstyle="->"), fontsize = 'medium', horizontalalignment='left', verticalalignment='top')
        self.annot3.set_visible(False)


        def update_annotation(coords, type):
                self.annot.xy = coords
                if type == 'story':
                    self.annot3.xy = coords
                
                for index, row in WSDF.iterrows():
                    if ((row[self.dropdown1.currentText()] == coords[0]) and (row[self.dropdown2.currentText()] == coords[1])):
                        self.annot2.xy = (row[self.dropdown12.currentText()], row[self.dropdown22.currentText()])
                        self.annot.set_text("{}".format(row['Play']))
                        self.annot2.set_text("{}".format(row['Play']))
                        if type == 'story':
                            self.annot3.set_text("{}".format(row['Play']))
                        self.myPoint = row
                        break
                
                self.annot.get_bbox_patch().set_alpha(0.8)
                self.annot2.get_bbox_patch().set_alpha(0.8)
                self.annot3.get_bbox_patch().set_alpha(0.8)
                #annot.set_text("Gork Pingis Tricentennial")



        def popup_point(coords, type):
            popup = PointDialog(points=coords, parent=self)
            popup.exec()



        def motion_hover(event):
            if self.press:
                self.move=True
            vis = self.annot.get_visible()
            if event.inaxes == self.sc.axes:
                contPort, indPort = self.myPoints.contains(event)
                if contPort:
                    #print(self.myPoints.get_offsets()[indPort["ind"][0]])
                    update_annotation(self.myPoints.get_offsets()[indPort["ind"][0]], 'graph1')
                    self.annot.set_visible(True)
                    self.annot2.set_visible(True)
                    self.sc.fig.canvas.draw_idle()
                    self.sc2.fig.canvas.draw_idle()
                else:
                    if vis:
                        self.annot.set_visible(False)
                        self.annot2.set_visible(False)
                        self.sc.fig.canvas.draw_idle()
                        self.sc2.fig.canvas.draw_idle()
            if self.storyMode:
                if event.inaxes == self.sc3.axes:
                    contPort, indPort = self.storyPoints.contains(event)
                    if contPort:
                        #print(self.storyPoints.get_offsets()[indPort["ind"][0]])
                        update_annotation(self.storyPoints.get_offsets()[indPort["ind"][0]], 'story')
                        self.annot3.set_visible(True)
                        self.sc3.fig.canvas.draw_idle()

        def on_point_click(event, mode):
            if mode == 'story':
                if event.inaxes == self.sc3.axes:
                    if event.button == 1:
                        contPort, indPort = self.storyPoints.contains(event)
                        if contPort:
                            popup_point(self.storyPoints.get_offsets()[indPort["ind"][0]], "story")
                    if event.button == 3:
                        self.find_closest_points(self.storyPoints.get_offsets()[indPort["ind"][0]])
            elif event.inaxes == self.sc.axes:
                contPort, indPort = self.myPoints.contains(event)
                if event.button == 1: #left click
                    if contPort:
                        print(self.myPoints.get_offsets()[indPort["ind"][0]])
                        popup_point(self.myPoints.get_offsets()[indPort["ind"][0]], 'graph1')
                if event.button == 3: #right click
                    self.find_closest_points(self.myPoints.get_offsets()[indPort["ind"][0]])
                    print("I am r")


        def on_press(event):
            self.press=True

        def on_release(event):
            if self.press and not self.move:
                on_point_click(event, 'normal')
            self.press=False; self.move=False

        
        #story functions
        def on_release_story(event):
            if self.press and not self.move:
                on_point_click(event, 'story')
            self.press=False; self.move=False

        def on_key_press(event):
                    print('press', event.key)
                    if event.key == 'right':
                        go_right()
                    if event.key == 'left':
                        go_left()

        def go_right():
            self.game = self.game + 1
            if self.game == self.games[-1] + 1:
                self.create_graph(self.game)
            elif self.game > self.games[-1]:
                self.leave_storymode()
            else:
                self.create_graph(self.game)

        def go_left():
            self.game = self.game - 1
            if self.game < self.games[0]:
                self.game = self.game + 1 #do nothing
            else:
                self.create_graph(self.game)

        self.sc3.fig.canvas.mpl_connect('key_press_event', on_key_press)
        self.sc3.fig.canvas.mpl_connect('motion_notify_event', motion_hover)
        self.sc3.fig.canvas.mpl_connect('button_press_event', on_press)
        self.sc3.fig.canvas.mpl_connect('button_release_event', on_release_story)


        def narrativeGUI():
            theGrid = NarrativeDialog()
            if theGrid.exec():
                print("success")
                self.sc3.fig.canvas.setFocusPolicy( QtCore.Qt.ClickFocus )
                self.sc3.fig.canvas.setFocus()
                #Hide the bottom layers so that we only see the middle pane
                self.secondFrame.hide()
                self.firstFrame.hide()
                self.setWindowTitle(theGrid.selectWS.currentText())
                #Create a new MPL Canvas and draw it in the spot of the sc, on game 1 of the selected world series
                WSYear = int(theGrid.selectWS.currentText()[:4])
                self.storyDF = WSDF.loc[WSDF['Year'] == WSYear]
                self.games = sorted(self.storyDF['Game'].unique())
                self.game = 1
                self.storyMode = True
                print(self.games)
                self.thirdFrame.show()
                self.myCMAP = matplotlib.cm.RdBu_r
                
                self.create_graph(self.game)
                #QtWidgets.QApplication.processEvents()

                
                
                #Desired animation - Preprocess biggest play in the game, determined by chosen axes (this case LI and WPA). Showcase highest LI and highest WPA in game, as well as overall (euclidean) best point

                #When we have 2-3 biggest points, speed through game sequentially, slowing down and highlighting the biggest points maybe with a annotation for more info.

                #Allow for a click (right) to transition to next game at any time in the process. (might have to disconnect and reconnect to new function)
        
        
                #End things:

                #self.thirdFrame.hide()
                #self.firstFrame.show()
                #self.setWindowTitle("World Series Visualization")
            else:
                print("fail")





        self.narrative.clicked.connect(narrativeGUI)
        self.sc.fig.canvas.mpl_connect('motion_notify_event', motion_hover)
        self.sc.fig.canvas.mpl_connect('button_press_event', on_press)
        self.sc.fig.canvas.mpl_connect('button_release_event', on_release)



        






        self.show() #end init

    def find_closest_points(self, npoints):
        closestPoint = []
        baseLine = [self.myPoint['LI'] + self.myPoint['WPA'] + self.myPoint['RE'] + self.myPoint['RE24']]
        
        mindist = 999999
        maxes = [WSDF['LI'].max(), WSDF['WPA'].max(), WSDF['RE'].max(), WSDF['RE24'].max()]
        baseProps = [bl / m for bl, m in zip(baseLine, maxes)]
        for index, row in WSDF.iterrows():
            dist = 0
            line = [row['LI'] + row['WPA'] + row['RE'] + row['RE24']]
            props = [l / m for l, m in zip(line, maxes)]
            for i in range(0, len(props)):
                dist = dist + abs(props[i] - baseProps[i])

        
            if dist < mindist:
                print(dist)
                if dist != 0:
                    closestPoint = row
                    mindist = dist
        print(closestPoint)
        dlg = PointDialog(closestPoint, isNeighbor=True, parent=self)
        dlg.setWindowTitle("Closest At-Bat")
        dlg.exec()


    def leave_storymode(self):
        self.sc3.axes.clear()
        self.thirdFrame.hide()
        self.firstFrame.show()
        self.storyMode = False
        if self.graph2Button.text() == 'Hide Extra Graph':
            self.secondFrame.show()

    def create_graph(self, game):
        self.sc3.axes.clear()
        if game > self.games[-1]:
            WSGamedf = self.storyDF
            self.sc3.axes.set_title('Series Summary\n(Exit with Right Arrow, Return with Left Arrow)'.format(game))
        else :
            WSGamedf = self.storyDF.loc[self.storyDF['Game'] == game]
            self.sc3.axes.set_title('Game {}\n(Advance with Right Arrow, Return with Left Arrow)'.format(game))
        minWPA = WSGamedf['WPA'].min()
        maxWPA = WSGamedf['WPA'].max()
        myMid =  1 - maxWPA / (maxWPA + abs(minWPA))
        newCMAP = self.shiftedColorMap(cmap=self.myCMAP, midpoint=myMid, name='gameCMAP')
        
        self.storyPoints = self.sc3.axes.scatter(WSGamedf['WPA'], WSGamedf['LI'], alpha=.5, c=WSGamedf['WPA'], cmap=newCMAP)#, s=WSDF['population']/1000000, alpha=.5, c=WSDF['life_expectancy'])
        
        self.sc3.axes.set_xlabel('WPA')
        self.sc3.axes.set_ylabel('LI')
        self.annot3 = self.sc3.axes.annotate("", xy=(1, 4), xytext=(0.0125, 0.975),
                textcoords='axes fraction',
                bbox=dict(boxstyle="round", fc="w"), annotation_clip=True,
                arrowprops=dict(arrowstyle="->"), fontsize = 'large', horizontalalignment='left', verticalalignment='top')
        self.annot3.set_visible(False)
        self.sc3.draw()


    def filterGraph1(self):
        dlg = CustomDialog(self)
        dlg.setWindowTitle("Uncheck Boxes you'd like to Filter Out")
        if dlg.exec():
            print("Success!")
            
            filteredYears = []
            filteredInnings = []
            filteredGames = []
            filteredEvents = []
            for year in dlg.yearCheckBox:
                if year.isChecked():
                    filteredYears.append(int(year.text()))

            for Inning in dlg.InningCheckBox:
                if Inning.isChecked():
                    if(Inning.text() == '13+'):
                        filteredInnings.extend([13, 14, 15, 16, 17, 18])
                        continue
                    filteredInnings.append(int(Inning.text()))


            for game in dlg.gameCheckBox:
                if game.isChecked():
                    filteredGames.append(int(game.text().split()[1]))

            for event in dlg.eventCheckBox:
                if event.isChecked():
                    filteredEvents.append(event.text())

            filterDF = WSDF
            print(filterDF['InningNum'].head())
            filterDF = filterDF.loc[filterDF['Year'].isin(filteredYears)]
            
            filterDF = filterDF.loc[filterDF['InningNum'].isin(filteredInnings)]
            filterDF = filterDF.loc[filterDF['Game'].isin(filteredGames)]
            if 'Other' in filteredEvents:
                otherPlays = np.setdiff1d(WSDF['lastEvent'].unique(), np.array(['Single', 'Double', 'Triple', 'Home Run', 'Walk', 'Strikeout', 'Stolen Base']))
                filteredEvents.extend(otherPlays)
            filterDF = filterDF.loc[filterDF['lastEvent'].isin(filteredEvents)]

            self.sc.axes.clear() #clear
            self.myPoints = self.sc.axes.scatter(filterDF[str(self.dropdown1.currentText())], filterDF[str(self.dropdown2.currentText())],alpha=.5, c=filterDF[str(self.dropdown3.currentText())])
            self.sc.axes.set_ylabel(str(self.dropdown2.currentText()))
            self.sc.axes.set_xlabel(str(self.dropdown1.currentText()))
            self.annot = self.sc.axes.annotate("", xy=(1, 4), xytext=(0.0125, 0.975),
            textcoords='axes fraction',
                            bbox=dict(boxstyle="round", fc="w"), annotation_clip=True,
                            arrowprops=dict(arrowstyle="->"), fontsize='medium', horizontalalignment='left', verticalalignment='top')

            if self.graph2Button.text() == 'Hide Extra Graph':
                self.annot.set_fontsize('small')

            self.annot.set_visible(False)
            self.sc.draw()

            #2
            self.sc2.axes.clear() #clear
            self.sc2.axes.scatter(filterDF[str(self.dropdown12.currentText())], filterDF[str(self.dropdown22.currentText())],alpha=.5)
            self.sc2.axes.set_ylabel(str(self.dropdown22.currentText()))
            self.sc2.axes.set_xlabel(str(self.dropdown12.currentText()))
            self.annot2 = self.sc2.axes.annotate("", xy=(1, 4), xytext=(0.0125, 0.975),
            textcoords='axes fraction',
                            bbox=dict(boxstyle="round", fc="w"), annotation_clip=True,
                            arrowprops=dict(arrowstyle="->"), fontsize='small', horizontalalignment='left', verticalalignment='top')



            self.annot2.set_visible(False)
            self.sc2.draw()

            currWSDF = filterDF
            #print(filteredYears)
            #print(filteredInnings)
            #print(filteredGames)
            #print(filteredEvents)


        else:
            print("Cancel!")

    def graph2visibility(self):
        if self.graph2Button.text() == 'Reveal Extra Graph':
            self.annot.set_fontsize('small')
            self.secondFrame.show()
            self.graph2Button.setText('Hide Extra Graph')
        else:
            self.annot.set_fontsize('medium')
            self.secondFrame.hide()
            self.graph2Button.setText('Reveal Extra Graph')

    def update_graph(self):
        vars = [str(self.dropdown1.currentText()), str(self.dropdown2.currentText()), str(self.dropdown3.currentText())]
        self.sc.axes.clear() #clear
        self.sc.axes.scatter(WSDF[vars[0]], WSDF[vars[1]],alpha=.5, c=WSDF[vars[2]])# s=WSDF[vars[2]]/1000000)#)
        
        self.sc.axes.set_ylabel(vars[1])
        self.sc.axes.set_xlabel(vars[0])
        self.annot = self.sc.axes.annotate("", xy=(1, 4), xytext=(0.0125, 0.975),
                textcoords='axes fraction',
                bbox=dict(boxstyle="round", fc="w"), annotation_clip=True,
                arrowprops=dict(arrowstyle="->"), fontsize = 'medium', horizontalalignment='left', verticalalignment='top')
        if(self.graph2Button.text() == 'Hide Extra Graph'):
            self.annot.set_fontsize('small')
        self.annot.set_visible(False)
        self.sc.draw() #WE DID IT

    def update_graph2(self):
        vars = [str(self.dropdown12.currentText()), str(self.dropdown22.currentText()), str(self.dropdown32.currentText())]
        self.sc2.axes.clear() #clear
        self.sc2.axes.scatter(WSDF[vars[0]], WSDF[vars[1]], alpha=.5, c=WSDF[vars[2]])# s=WSDF[vars[2]]/1000000)#, c=WSDF[vars[3]])
        
        self.sc2.axes.set_ylabel(vars[1])
        self.sc2.axes.set_xlabel(vars[0])
        self.annot2 = self.sc2.axes.annotate("", xy=(1, 4), xytext=(0.0125, 0.975),
                textcoords='axes fraction',
                bbox=dict(boxstyle="round", fc="w"), annotation_clip=True,
                arrowprops=dict(arrowstyle="->"), fontsize = 'small', horizontalalignment='left', verticalalignment='top')
        self.annot2.set_visible(False)
        self.sc2.draw() #WE DID IT    

    #def scaleArea(self, value):
    #    vars = [str(self.dropdown1.currentText()), str(self.dropdown2.currentText()), str(self.dropdown3.currentText())]
    #    self.sc.axes.clear() #clear
    #    self.sc.axes.scatter(WSDF[vars[0]], WSDF[vars[1]], s=value, alpha=.5, c=WSDF[vars[2]])
    #    self.sc.axes.set_ylabel(vars[1])
    #    self.sc.axes.set_xlabel(vars[0])
    #   self.sc.draw() #WE DID IT
        
    #def scaleArea2(self, value):
    #    vars = [str(self.dropdown12.currentText()), str(self.dropdown22.currentText()), str(self.dropdown32.currentText())]
    #    self.sc2.axes.clear() #clear
    #    self.sc2.axes.scatter(WSDF[vars[0]], WSDF[vars[1]], s=value, alpha=.5, c=WSDF[vars[2]])
    #    self.sc2.axes.set_ylabel(vars[1])
    #   self.sc2.axes.set_xlabel(vars[0])
    #    self.sc2.draw() #WE DID IT




    def shiftedColorMap(self, cmap=None, start=0, midpoint=0.5, stop=1.0, name='shiftedcmap'):
        '''
        Function to offset the "center" of a colormap. Useful for
        data with a negative min and positive max and you want the
        middle of the colormap's dynamic range to be at zero.

        Input
        -----
          cmap : The matplotlib colormap to be altered
          start : Offset from lowest point in the colormap's range.
              Defaults to 0.0 (no lower offset). Should be between
              0.0 and `midpoint`.
          midpoint : The new center of the colormap. Defaults to 
              0.5 (no shift). Should be between 0.0 and 1.0. In
              general, this should be  1 - vmax / (vmax + abs(vmin))
              For example if your data range from -15.0 to +5.0 and
              you want the center of the colormap at 0.0, `midpoint`
              should be set to  1 - 5/(5 + 15)) or 0.75
          stop : Offset from highest point in the colormap's range.
              Defaults to 1.0 (no upper offset). Should be between
              `midpoint` and 1.0.
        '''
        cdict = {
            'red': [],
            'green': [],
            'blue': [],
            'alpha': []
        }

        # regular index to compute the colors
        reg_index = np.linspace(start, stop, 257)

        # shifted index to match the data
        shift_index = np.hstack([
            np.linspace(0.0, midpoint, 128, endpoint=False), 
            np.linspace(midpoint, 1.0, 129, endpoint=True)
        ])

        for ri, si in zip(reg_index, shift_index):
            r, g, b, a = cmap(ri)

            cdict['red'].append((si, r, r))
            cdict['green'].append((si, g, g))
            cdict['blue'].append((si, b, b))
            cdict['alpha'].append((si, a, a))

        newcmap = matplotlib.colors.LinearSegmentedColormap(name, cdict)

        return newcmap
    



    


    
            






app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()
