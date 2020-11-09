import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')

from mpl_widget import Mpl_widget


class Main_window(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(Main_window, self).__init__()
        uic.loadUi(r"main_window.ui", self)
        self.addToolBar(NavigationToolbar(self.plot.canvas, self))
        self.show()


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    window = Main_window()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
