import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QDesktopWidget
from PyQt5.QtCore import QTimer

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

        self.interval_label = QLabel("Интервал (мс):")
        self.interval_input = QLineEdit()
        self.layout.addWidget(self.interval_label)
        self.layout.addWidget(self.interval_input)

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

        # Кнопки
        self.button_group = QWidget()
        self.button_layout = QVBoxLayout()

        self.realtime_button = QPushButton("Запустить в реальном времени")
        self.button_layout.addWidget(self.realtime_button)
        self.realtime_button.clicked.connect(self.run_realtime_simulation)


        self.pause_button = QPushButton("Пауза")
        self.button_layout.addWidget(self.pause_button)
        self.pause_button.clicked.connect(self.pause_simulation)
        self.pause_button.setEnabled(False)

        self.resume_button = QPushButton("Продолжить")
        self.button_layout.addWidget(self.resume_button)
        self.resume_button.clicked.connect(self.resume_simulation)
        self.resume_button.setEnabled(False)

        self.new_plot_button = QPushButton("Новый график")
        self.button_layout.addWidget(self.new_plot_button)
        self.new_plot_button.clicked.connect(self.new_plot)
        self.new_plot_button.setEnabled(False)

        self.button_group.setLayout(self.button_layout)
        self.layout.addWidget(self.button_group)
        self.run_button = QPushButton("Запустить")
        self.layout.addWidget(self.run_button)
        self.run_button.clicked.connect(self.run_simulation)

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_realtime_plot)

        self.is_paused = False
        self.interval = 10  # Интервал между обновлениями графика в миллисекундах

        self.fixed_time_label = QLabel("Фиксированное время (мс):")
        self.fixed_time_input = QLineEdit()
        self.layout.addWidget(self.fixed_time_label)
        self.layout.addWidget(self.fixed_time_input)

        self.fixed_time = 1000  # Значение фиксированного времени по умолчанию
        self.iteration_count = 0  # Переменная для подсчета итераций

        self.setLayout(self.layout)



    def run_realtime_simulation(self):
        if self.timer.isActive():
            return
        self.interval = int(self.interval_input.text())

        # Проверка ввода для интервала
        try:
            self.interval = int(self.interval_input.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Некорректный ввод для интервала.")
            return

        fixed_time_text = self.fixed_time_input.text()
        if fixed_time_text:
            try:
                self.fixed_time = int(fixed_time_text)
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Некорректный ввод для фиксированного времени.")
                return
        else:
            self.fixed_time = 1000  # Значение фиксированного времени по умолчанию

        # Проверка ввода для коэффициентов
        try:
            a1 = float(self.a1_input.text())
            a2 = float(self.a2_input.text())
            b1 = float(self.b1_input.text())
            b2 = float(self.b2_input.text())
            b3 = float(self.b3_input.text())
            c1 = float(self.c1_input.text())
            c2 = float(self.c2_input.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Некорректный ввод для коэффициентов.")
            return

        # Проверка ввода для начальных условий
        try:
            V0 = float(self.V0_input.text())
            P0 = float(self.P0_input.text())
            R0 = float(self.R0_input.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Некорректный ввод для начальных условий.")
            return

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
        self.V = V
        self.P = P
        self.R = R
        self.idx = 0

        self.ax.clear()
        self.ax.set_xlabel('V')
        self.ax.set_ylabel('P')
        self.ax.set_zlabel('R')

        self.realtime_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.resume_button.setEnabled(False)
        self.new_plot_button.setEnabled(False)

        self.timer.start(self.interval)
        self.fig.show()


    def pause_simulation(self):
        if self.timer.isActive():

            self.timer.stop()
            self.pause_button.setEnabled(False)
            self.resume_button.setEnabled(True)
            self.new_plot_button.setEnabled(True)
            self.is_paused = True

    def resume_simulation(self):
        if not self.timer.isActive() and self.is_paused:

            self.timer.start(self.interval)
            self.pause_button.setEnabled(True)
            self.resume_button.setEnabled(False)
            self.new_plot_button.setEnabled(False)
            self.is_paused = False

    def update_realtime_plot(self):
        self.iteration_count += 1  # Увеличение счетчика итераций
        # Обновление графика в реальном времени
        try:
            self.ax.plot([self.V[self.idx-1], self.V[self.idx]], [self.P[self.idx-1], self.P[self.idx]], [self.R[self.idx-1], self.R[self.idx]], 'b-')

            self.idx += 1
            self.fig.canvas.draw()
        except IndexError:
            self.timer.stop()
            self.realtime_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.resume_button.setEnabled(False)
            self.new_plot_button.setEnabled(True)
            final_time = self.idx * self.interval
            final_coordinates = (
                round(self.V[self.idx - 1], 3),
                round(self.P[self.idx - 1], 3),
                round(self.R[self.idx - 1], 3)
            )
            QMessageBox.information(self, "Результаты", f"Точное время отрисовки: {final_time} мс\n"
                                                        f"Финальные координаты: {final_coordinates}")
        if self.fixed_time is not None and (self.idx * self.interval) >= self.fixed_time:
            self.timer.stop()
            self.realtime_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.resume_button.setEnabled(False)
            self.new_plot_button.setEnabled(True)
            final_time = self.idx * self.interval
            final_coordinates = (
                round(self.V[self.idx - 1], 3),
                round(self.P[self.idx - 1], 3),
                round(self.R[self.idx - 1], 3)
            )
            QMessageBox.information(self, "Результаты", f"Точное время отрисовки: {final_time} мс\n"
                                                        f"Финальные координаты: {final_coordinates}")
            self.iteration_count = 0
        elif self.fixed_time is None and self.iteration_count >= 1000:
            self.timer.stop()
            self.realtime_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.resume_button.setEnabled(False)
            self.new_plot_button.setEnabled(True)
            final_time = self.idx * self.interval
            final_coordinates = (
                round(self.V[self.idx - 1], 3),
                round(self.P[self.idx - 1], 3),
                round(self.R[self.idx - 1], 3)
            )
            QMessageBox.information(self, "Результаты", f"Точное время отрисовки: {final_time} мс\n"
                                                        f"Финальные координаты: {final_coordinates}")
            self.iteration_count = 0

    from PyQt5.QtWidgets import QMessageBox

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

        # Извлечение последних координат
        last_V = V[-1]
        last_P = P[-1]
        last_R = R[-1]

        # Формирование строки с округленными последними координатами
        coordinates = f"V={round(last_V, 3)}, P={round(last_P, 3)}, R={round(last_R, 3)}"

        # Вывод координат в QMessageBox
        QMessageBox.information(self, "Результаты", coordinates)

    def new_plot(self):
        self.realtime_button.setEnabled(True)
        self.new_plot_button.setEnabled(False)
        self.ax.clear()
        self.fig.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(150, 470, 100, 100)
    window.move(QDesktopWidget().availableGeometry().center() - window.frameGeometry().center())

    window.show()
    sys.exit(app.exec_())