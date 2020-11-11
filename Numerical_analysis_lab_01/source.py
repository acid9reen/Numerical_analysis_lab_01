import sys
import numpy as np
import random
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from Integrator.integrator import Integrator

matplotlib.use('Qt5Agg')


class Main_window(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(Main_window, self).__init__()
        uic.loadUi(r"Numerical_analysis_lab_01\main_window.ui", self)
        self.addToolBar(NavigationToolbar(self.plot.canvas, self))
        self.plot_btn.clicked.connect(self.update_graph)


    def update_graph(self):

        self.x_min = float(self.x_min_text_box.text())
        self.x_max = float(self.x_max_text_box.text())
        self.u_0   = float(self.u_0_text_box.text())
        self.step  = float(self.step_text_box.text())
        self.eps   = float(self.eps_text_box.text())
        self.max_iters = 1000

        if self.test_task_1_radio_btn.isChecked():
            integrator = Integrator(Integrator.test_task_1, self.step,
                                    self.eps, self.max_iters)
            x_curr = self.x_min
            v_curr = self.u_0
            xs = np.array([], dtype=np.longdouble)
            vs = np.array([], dtype=np.longdouble)
            us = np.array([], dtype=np.longdouble)

            row = 0
            while (self.table.rowCount() > 0):
                self.table.removeRow(0)

            while x_curr < self.x_max:
                if self.step_control_check_box.isChecked():
                    point_info = integrator.next_point_with_step_control(x_curr,
                                                                        v_curr)
                else:
                    point_info = integrator.next_point(x_curr, v_curr)

                self.table.insertRow(row)
                for index, item in enumerate(point_info.all()):
                    self.table.setItem(row, index, QtWidgets.QTableWidgetItem(
                        f"{item:.2e}" if isinstance(item, float) else f"{item}"))

                row += 1

                x_curr = point_info.x
                v_curr = point_info.v
                xs = np.append(xs, x_curr)
                vs = np.append(vs, v_curr)
                us = np.append(us, Integrator.test_task_1_true_solution(x_curr, v_curr))

            self.table.setVerticalHeaderLabels((str(i) for i in range(row + 1)))
            self.plot.canvas.axes.clear()
            self.plot.canvas.axes.plot(xs, vs)
            self.plot.canvas.axes.plot(xs, us)
            self.plot.canvas.axes.legend(('v(x)', 'u(x)'),loc='upper right')
            self.plot.canvas.axes.set_title('Numerical approximation')
            self.plot.canvas.draw()

        elif self.task_1_radio_btn.isChecked():
            integrator = Integrator(Integrator.task_1, self.step,
                                    self.eps, self.max_iters)
            x_curr = self.x_min
            v_curr = self.u_0
            xs = np.array([], dtype=np.longdouble)
            vs = np.array([], dtype=np.longdouble)

            row = 0
            while (self.table.rowCount() > 0):
                self.table.removeRow(0)

            while x_curr < self.x_max:
                if self.step_control_check_box.isChecked():
                    point_info = integrator.next_point_with_step_control(x_curr,
                                                                        v_curr)
                else:
                    point_info = integrator.next_point(x_curr, v_curr)

                self.table.insertRow(row)
                for index, item in enumerate(point_info.all()):
                    self.table.setItem(row, index, QtWidgets.QTableWidgetItem(
                        f"{item:.2e}" if isinstance(item, float) else f"{item}"))

                row += 1

                x_curr = point_info.x
                v_curr = point_info.v
                xs = np.append(xs, x_curr)
                vs = np.append(vs, v_curr)

            self.table.setVerticalHeaderLabels((str(i) for i in range(row + 1)))
            self.plot.canvas.axes.clear()
            self.plot.canvas.axes.plot(xs, vs)
            self.plot.canvas.axes.legend(('v(x)'),loc='upper right')
            self.plot.canvas.axes.set_title('Numerical approximation')
            self.plot.canvas.draw()


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    window = Main_window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
