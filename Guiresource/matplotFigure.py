from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(PlotCanvas, self).__init__(self.fig)
        self.setParent(parent)

        self.pltCnt = 0
        self.twinxList= []
        
    def clearPlot(self):
        for twin in self.twinxList:
            self.fig.delaxes(twin)
        self.axes.clear()
        self.twinxList = []
        self.draw()
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
        self.draw()


        self.pltCnt+=1
