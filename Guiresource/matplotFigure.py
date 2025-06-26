from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt6.QtWidgets import QWidget

class PlotCanvas(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create the figure and canvas
        self.fig= Figure()
        self.canvas = FigureCanvas(self.fig)
        
        # Create the navigation toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.pltCnt = 0
        self.twinxList= []

        self.axes = self.fig.add_subplot(111)
        
    def clearPlot(self):
        for twin in self.twinxList:
            self.fig.delaxes(twin)
        self.axes.clear()
        self.twinxList = []


        self.canvas.draw()
        self.pltCnt = 0
    
    def plot(self,Data, label):
        unit = None
        if "(" in label:
            unit = label.split("(")[-1]
            unit = unit[:-1]
        
        if unit:
            twin = self.axes.twinx()
            self.twinxList.append(twin)
            twin.spines["right"].set_position(("axes", len(self.twinxList)*0.1+0.9))
            twin.plot(Data,color= f"C{self.pltCnt}", label = label, alpha =0.7)
            twin.set_ylabel(unit, color = f"C{self.pltCnt}")
                               
            twin.tick_params(axis='y', colors=f"C{self.pltCnt}")
            twin.spines["right"].set_edgecolor(f"C{self.pltCnt}")
            
        else:
            self.axes.plot(Data, color= f"C{self.pltCnt}",label = label, alpha= 0.7)
        
        self.axes.legend()
        # Refresh canvas
        self.fig.tight_layout()
        self.axes.grid(True)
        self.canvas.draw()


        self.pltCnt+=1
