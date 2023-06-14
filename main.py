import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout


# Функция, описывающая систему дифференциальных уравнений
def system(t, variables, a1, a2, b1, b2, b3, c1, c2):
    V, P, R = variables

    dV_dt = a1 * V - a2 * V * P
    dP_dt = b1 * V * P - b2 * P - b3 * P * R
    dR_dt = c1 * P * R - c2 * R

    return [dV_dt, dP_dt, dR_dt]


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Решение системы дифференциальных уравнений")
        self.layout = QVBoxLayout()

        # Ввод коэффициентов
        self.a1_label = QLabel("a1:")
        self.a1_input = QLineEdit()
        self.layout.addWidget(self.a1_label)
        self.layout.addWidget(self.a1_input)

        self.a2_label = QLabel("a2:")
        self.a2_input = QLineEdit()
        self.layout.addWidget(self.a2_label)
        self.layout.addWidget(self.a2_input)

        self.b1_label = QLabel("b1:")
        self.b1_input = QLineEdit()
        self.layout.addWidget(self.b1_label)
        self.layout.addWidget(self.b1_input)

        self.b2_label = QLabel("b2:")
        self.b2_input = QLineEdit()
        self.layout.addWidget(self.b2_label)
        self.layout.addWidget(self.b2_input)

        self.b3_label = QLabel("b3:")
        self.b3_input = QLineEdit()
        self.layout.addWidget(self.b3_label)
        self.layout.addWidget(self.b3_input)

        self.c1_label = QLabel("c1:")
        self.c1_input = QLineEdit()
        self.layout.addWidget(self.c1_label)
        self.layout.addWidget(self.c1_input)

        self.c2_label = QLabel("c2:")
        self.c2_input = QLineEdit()
        self.layout.addWidget(self.c2_label)
        self.layout.addWidget(self.c2_input)

        # Начальные условия
        self.V0_label = QLabel("Начальное значение V:")
        self.V0_input = QLineEdit()
        self.layout.addWidget(self.V0_label)
        self.layout.addWidget(self.V0_input)

        self.P0_label = QLabel("Начальное значение P:")
        self.P0_input = QLineEdit()
        self.layout.addWidget(self.P0_label)
        self.layout.addWidget(self.P0_input)

        self.R0_label = QLabel("Начальное значение R:")
        self.R0_input = QLineEdit()
        self.layout.addWidget(self.R0_label)
        self.layout.addWidget(self.R0_input)

        # Кнопка запуска
        self.run_button = QPushButton("Запустить")
        self.layout.addWidget(self.run_button)
        self.run_button.clicked.connect(self.run_simulation)

        self.setLayout(self.layout)

    def run_simulation(self):
        # Извлечение введенных данных
        a1 = float(self.a1_input.text())
        a2 = float(self.a2_input.text())
        b1 = float(self.b1_input.text())
        b2 = float(self.b2_input.text())
        b3 = float(self.b3_input.text())
        c1 = float(self.c1_input.text())
        c2 = float(self.c2_input.text())
        V0 = float(self.V0_input.text())
        P0 = float(self.P0_input.text())
        R0 = float(self.R0_input.text())

        # Временные точки для интегрирования
        t_start = 0
        t_end = 10
        t_points = np.linspace(t_start, t_end, 1000)

        # Решение системы дифференциальных уравнений
        solution = solve_ivp(system, [t_start, t_end], [V0, P0, R0], t_eval=t_points,
                             args=(a1, a2, b1, b2, b3, c1, c2))

        # Извлечение решения
        V = solution.y[0]
        P = solution.y[1]
        R = solution.y[2]

        # Визуализация результата
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(V, P, R)
        ax.set_xlabel('V')
        ax.set_ylabel('P')
        ax.set_zlabel('R')
        plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
