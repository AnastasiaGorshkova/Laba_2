from matplotlib import pyplot
from scipy.signal import savgol_filter
import numpy
from textwrap import wrap
import matplotlib.ticker as ticker
#https://pyprog.pro/mpl/mpl_main_components.html

# P = 0.099 * N - 7.24 [мм рт.ст]
def Pressure(N):
    P = 0.099 * N - 7.24
    return P

with open("NastyaG.txt", "r") as file:
    array_rest_pressure_1 = [Pressure(int(i)) for i in file.read().split("\n")]

array_rest_pressure = []
for i in range(0, len(array_rest_pressure_1),50):
    array_rest_pressure.append(array_rest_pressure_1[i])

array_time = []
for i in range(0, len(array_rest_pressure)):
    array_time.append(i*(60 / len(array_rest_pressure)))

#Создаём массив точек прямой: y = kx + c c = y1 - k * x1 ; k = (y2 - y1) / (x2 - x1)
y1 = 84
x1 = 11.65
y2 = 81
x2 = 12.30
k = (y2-y1) / (x2 - x1)
c = y1 - k * x1
for i in range(0, len(array_rest_pressure)):
    array_rest_pressure[i] -= (array_time[i] * k + c)

# #Создаём апркосимирующую прямую
# aproxim = savgol_filter(array_rest_pressure, 600, 1)
# for i in range(0, len(aproxim)):
#     aproxim[i] = aproxim[i] - 1
#
# #Создаём массив разностей апроксимации и значений для выявления изменения давления:
# for i in range(0, len(array_rest_pressure)):
#     array_rest_pressure[i] -= aproxim[i]

#оздаём апроксимацию данных изменения давления
aproxim_delta = savgol_filter(array_rest_pressure, 40, 1)

#Чёрная линия
massive = []
for l in range(0, len(array_rest_pressure)):
    massive.append(0)

#считываем показания в 4-ёх состояниях
data = numpy.array(array_rest_pressure)
data_0 = numpy.array(aproxim_delta)
data_dark = numpy.array(massive)

#считываем показания
data_time = numpy.array(array_time)
#параметры фигуры
fig, ax = pyplot.subplots(figsize=(16, 9), dpi=500)

#минимальные и максимальные значения для осей
ax.axis([12.8, 13.7 + 0, 0.2, 2])

#Включаем видимость сетки и делений (вводим их параметры ниже(сверху нельзя)
ax.minorticks_on()

#  Устанавливаем интервал основных делений:
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
#  Устанавливаем интервал вспомогательных делений:
ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.01))

#  Тоже самое проделываем с делениями на оси "y":
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.05))

#Устанавливаем параметры подписей делений: https://pyprog.pro/mpl/mpl_axis_ticks.html
ax.tick_params(axis = 'both', which = 'major', labelsize = 15, pad = 2, length = 10)
ax.tick_params(axis = 'both', which = 'minor', labelsize = 15, pad = 2, length = 5)

#название графика с условием для переноса строки и центрированием
ax.set_title("\n".join(wrap('Артериальное давление в спокойном состоянии (Настя)', 80)), fontsize = 25, pad = 20, loc = 'center')

#сетка основная и второстепенная
ax.grid(which='major', color = 'gray')
ax.grid(which='minor', color = 'gray', linestyle = '--')


#подпись осей
ax.set_ylabel("Изменение давления [мм рт.ст.]", fontsize = 16)
ax.set_xlabel("Время [с]", fontsize = 16)

#маркеры
ax.scatter(5.6, 126.4, marker ='o', c ='blue', s=80)
ax.scatter(12.3, 81, marker ='o', c ='blue', s=80)

#Добавление самого графика и (в конце присваивает наличие леге label =...)
ax.plot(data_time, data, c='m', linewidth=2, label ='Давление - 126/81 [мм рт.ст.]')
ax.plot(data_time, data_0, c='blue', linewidth=3, label ='Апроксимация')
ax.plot(data_time, data_dark, c='k', linewidth=2)

#Добавил маркеры в легенду с надписью измерения

#Добавление легенды: https://pyprog.pro/mpl/mpl_adding_a_legend.html
ax.legend(shadow = False, loc = 'upper right', fontsize = 17)

#Добавление текста  https://pyprog.pro/mpl/mpl_text.html
ax.text(13.05, 0.6, 'a = 1.4 мм рт.ст; t(systole) = 0.45 с', rotation = 0, fontsize = 33)
ax.text(13.05, 0.4, 'b = 0.8 мм рт.ст; t(diastole) = 0.21 с', rotation = 0, fontsize = 33)
ax.text(13.05, 0.22, 'dt = 0.35 c', rotation = 0, fontsize = 33)

#сохранение
fig.savefig('rest-pressure-2.png')
