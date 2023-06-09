'''
Простейшая реализация нейрона - персептрон  
Александр Степанов 07.05.2018
'''

# Данные для обучения персептрона.
# Представляют из себя словарь, ключом которого является цифра,
# отображение которой закодировано последовательностью нулей и единиц
# (рассматривайте последовательность как таблицу 3х5)
#
# Примеры цифр:
#
#  (0)     (1)     (2)
#
# 1 1 1   0 0 1   1 1 1
# 1 0 1   0 0 1   0 0 1
# 1 0 1   0 0 1   1 1 1
# 1 0 1   0 0 1   1 0 0
# 1 1 1   0 0 1   1 1 1
#
training_data = {
0: (1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1),
1: (0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1),
2: (1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1),
3: (1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1),
4: (1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1),
5: (1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1),
6: (1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1),
7: (1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1),
8: (1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1),
9: (1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1)}


# Класс Персептрон, чтобы мы могли создать нужное нам количество экземпляров персептронов
class perceptron:
    # Конструктор класса, где:
    # input_nodes_val - количество входов персептрона
    # init_weight - начальное значение весовых коэффициентов для входов
    # bias_val - пороговое значение для функции сравнения нейрона
    def __init__(self, input_nodes_val=15, init_weight=0, bias_val=8):
        self.bias = bias_val
        self.weights = []
        for i in range(input_nodes_val):
            self.weights.append(init_weight)

    # Здесь описана основная логика персептрона
    # Получаем данные из входного сигнала для каждого входа персептрона,
    # умножаем данные каждого входа на соответствующий ему весовой коэффициент,
    # суммируем все результаты и формируем выходной сигнал персептрона в соответствии
    # с заданным порогом. У нас бинарная пороговая функция, порог описан переменной bias
    def proceed(self, in_signal):
        net = 0
        for in_node in range(len(self.weights)):
            net += in_signal[in_node] * self.weights[in_node]
        return net >= self.bias

    # Ложное положительное срабатывание.
    # Иными словами, персептрон ошибся, выдал положительный ответ на неправильных данных.
    # Следовательно, мы должны понизить коэффициенты на входах, которые привели к положительному срабатыванию!
    def false_positive(self, in_signal):
        for in_node in range(len(self.weights)):
            if in_signal[in_node]:
                self.weights[in_node] -= 1

    # Ложное отрицательное срабатывание.
    # Персептрон ошибся, выдал отрицательный ответ на правильных данных!
    # Следовательно, мы должны увеличить коэффициенты на входах, которые привели к отрицательному срабатыванию!
    def false_negative(self, in_signal):
        for in_node in range(len(self.weights)):
            if in_signal[in_node]:
                self.weights[in_node] += 1

    # Позвращает коэффициенты
    def get_weights(self):
        return self.weights


# Итак, создадим 10 персептронов по количеству демонстрируемых цифр.
# Каждый персептрон будем обучать на "своей" цифре. Т.е., мы решаем, что нулевой персептрон это цифра 0,
# 1 - цифра 1 и т.д. Порядок можно сделать любым, но для нас проще будет именно так.
# Все обучение персептрона сводится к вызовам функций false_positive и false_negative на тренировочных данных,
# в результате чего весовые коэффиценты входов каждого из персептронов настраиваются на "свою" цифру,
# которую мы называем правильной. Благодаря этим действиям персептрон выделяет характерные признаки цифры.
# По сути весовые коэффициенты (множители входов) это и есть память нейросети.

neural_net = {}
for i in range(10):
    neural_net.update({i: perceptron()})

# Тренируем нашу нейростеть из десяти перцептронов
# Эпоха - полный цикл обучения нейросети (то есть, один полный проход по всем данным (цифрам)).
for epoch in range(50):     # Количество эпох
    for training_digit in range(10):     # Количество цифр на которых производим обучение (их 10)
        for num in range(10):   # Количество наших перцептронов (10 шт., по количеству цифр)
            if neural_net[num].proceed(training_data[training_digit]) and num != training_digit:
                neural_net[num].false_positive(training_data[training_digit])
            if not neural_net[num].proceed(training_data[training_digit]) and num == training_digit:
                neural_net[num].false_negative(training_data[training_digit])

print('\nОбучение закончено, посмотрим на весовые коэффициенты всех наших перцептронов!')
for i in range(10):
    print(i, '=', neural_net[i].get_weights())

print('\nОК, сделаем красивый вывод весовых коэффициентов вместе с данными на которых происходило обучение')
def print_train_perceptron(digit):
    print('\n======= Цифра %d =======' % digit)
    # цикл по строкам для вывода на печать
    for row in range(5):
        print('+---' * 3 + '+\t' + '+---' * 3 + '+')
        print('|%3d|%3d|%3d|\t|%3d|%3d|%3d|' % \
              (training_data[digit][row * 3], training_data[digit][row * 3 + 1], training_data[digit][row * 3 + 2],\
               neural_net[digit].get_weights()[row * 3], neural_net[digit].get_weights()[row * 3 + 1], neural_net[digit].get_weights()[row * 3 + 2]))
    print('+---' * 3 + '+\t' + '+---' * 3 + '+')

for i in range(10):
    print_train_perceptron(i)

print('\nОК, а теперь проверим работу нашей нейросети на тренировочных данных!'\
      '\nРяды - перцептроны по порядку, строки - подаваемое значение на вход\n')

print('=' * 50)
print('№ Нейрона:\t0\t1\t2\t3\t4\t5\t6\t7\t8\t9')
print('-' * 50)
for row in range(10):
    out_str = ("Число: %d" % row)
    for perc in range(10):
        out_str = out_str + ('\t%d' % neural_net[perc].proceed(training_data[row]))
    print(out_str)


# А теперь проверим на данных, которые нейросеть никогда не встречала!
# Мы скопируем и исказим тренировочные данные и скормим их нейросети перцептронов
test_data = {
0: (0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1),
1: (0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1),
2: (0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0),
3: (0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0),
4: (0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1),
5: (1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1),
6: (1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1),
7: (1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1),
8: (1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1),
9: (1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1)}


print('\nПроверим работу нашей нейросети на искаженных данных'\
      '\nНейросеть до этого их не встречала!')

print('=' * 50)
print('№ Нейрона:\t0\t1\t2\t3\t4\t5\t6\t7\t8\t9')
print('-' * 50)
for row in range(10):
    out_str = ("Число: %d" % row)
    for perc in range(10):
        out_str = out_str + ('\t%d' % neural_net[perc].proceed(test_data[row]))
    print(out_str)

print('Незначительное искажение входных данных (каждой цифры) не повлияло на результат!')

# Ну вот, Артем, без всяких сторониих библиотек мы создали перцептроны,
# обучили их и проверили в работе. Даже исполнилась твоя мечта - ты увидел что "видит" нейросеть ))
# Можешь поменять значение критерия пороговой функции (bias). Задается при создании класса, смотри конструктор.
# Также можно поменять количество эпох и оценить их влияение на результат.
# Ну и последнее - можно поиграть с внесением ошибок в test_data.
# Попытайся обмануть нейросеть зная ее весовые коэффициенты. Создай такие данные test_data, которые совершенно не будут
# похожи на цифры, но нейросеть их однозначно будет идентифицировать за нужную цифру.
# Подсказка: смотри на вывод таблиц весовых коэффициентов

def print_test_perceptron(digit):
    print('\n======= Цифра %d =======' % digit)
    # цикл по строкам для вывода на печать
    for row in range(5):
        print('+---' * 3 + '+\t' + '+---' * 3 + '+')
        print('|%3s|%3s|%3s|\t|%3d|%3d|%3d|' % \
              ('X' if test_data[digit][row * 3] > 0 else '', \
               'X' if test_data[digit][row * 3 + 1] > 0 else '', \
               'X' if test_data[digit][row * 3 + 2] > 0 else '',\
               neural_net[digit].get_weights()[row * 3], neural_net[digit].get_weights()[row * 3 + 1], neural_net[digit].get_weights()[row * 3 + 2]))
    print('+---' * 3 + '+\t' + '+---' * 3 + '+')

for i in range(10):
    print_test_perceptron(i)
