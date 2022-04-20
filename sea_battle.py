import copy
import random
import time


class SeaBattle:  # класс морского боя
    def __init__(self, boats=None, side=10, map_boats=None):  # инициализация
        self.last_my_shot = [0, 0]  # для записи выстрела
        sands_error = False
        self.is_complete = True
        start_time = time.time()  # расстановка кораблей
        while (time.time() - start_time) < 5:
            try:
                self.boats = list()
                if boats is None:
                    boats = [4, 3, 2, 1]
                for q in range(len(boats[::-1])):
                    self.boats += [len(boats[::-1]) - q] * (boats[::-1][q])
                self.side = side + 2
                self.my_map_boats = list()
                for q in range(self.side):
                    self.my_map_boats.append([None for _ in range(self.side)])
                self.enemy_map_shots = list()
                for q in range(self.side):
                    self.enemy_map_shots.append([None for _ in range(self.side)])
                no_place = False
                self.boats_dict = dict()
                num_iter = -1
                for q in self.boats:
                    num_iter += 1
                    for w in range(side ** 4):
                        a, b = random.randint(0, self.side - 1 - q + 1), random.randint(0, self.side - 1 - q + 1)
                        is_complete = True
                        coord_boats = list()
                        self.boats_dict_copy = dict()
                        if random.random() > 0.5:
                            for e in range(q):
                                if e == 0:
                                    if a - 1 >= 0 and b - 1 >= 0 and a + 1 < self.side and \
                                            b + 1 <= self.side - 1 and \
                                            self.my_map_boats[a][b] is None and \
                                            self.my_map_boats[a + 1][b] is None and \
                                            self.my_map_boats[a - 1][b] is None and \
                                            self.my_map_boats[a][b + 1] is None and \
                                            self.my_map_boats[a][b - 1] is None and \
                                            self.my_map_boats[a + 1][b + 1] is None and \
                                            self.my_map_boats[a + 1][b - 1] is None and \
                                            self.my_map_boats[a - 1][b + 1] is None and \
                                            self.my_map_boats[a - 1][b - 1] is None:
                                        coord_boats.append([a, b])
                                        self.boats_dict_copy[e] = [a, b]
                                    else:
                                        is_complete = False
                                else:
                                    if a + e + 1 < self.side and self.my_map_boats[a + e + 1][b] == \
                                            self.my_map_boats[a + e + 1][b - 1] == \
                                            self.my_map_boats[a + e + 1][
                                                b + 1] is None and a - 1 >= 0 and b - 1 >= 0 and b + e <= self.side - 1:
                                        coord_boats.append([a + e, b])
                                        self.boats_dict_copy[e] = [a + e, b]
                                    else:
                                        is_complete = False
                        else:
                            for e in range(q):
                                if e == 0:
                                    if a - 1 >= 0 and b - 1 >= 0 and a + 1 < self.side and \
                                            b + 1 <= self.side - 1 and \
                                            self.my_map_boats[a][b] is None and \
                                            self.my_map_boats[a + 1][b] is None and \
                                            self.my_map_boats[a - 1][b] is None and \
                                            self.my_map_boats[a][b + 1] is None and \
                                            self.my_map_boats[a][b - 1] is None and \
                                            self.my_map_boats[a + 1][b + 1] is None and \
                                            self.my_map_boats[a + 1][b - 1] is None and \
                                            self.my_map_boats[a - 1][b + 1] is None and \
                                            self.my_map_boats[a - 1][b - 1] is None:
                                        coord_boats.append([a, b])
                                        self.boats_dict_copy[e] = [a, b]
                                    else:
                                        is_complete = False
                                else:
                                    if b + e + 1 <= self.side - 1 and self.my_map_boats[a + 1][b + e + 1] == \
                                            self.my_map_boats[a][b + e + 1] == \
                                            self.my_map_boats[a - 1][
                                                b + e + 1] is None and a - 1 >= 0 and b - 1 >= 0 and a + e < \
                                            self.side:
                                        coord_boats.append([a, b + e])
                                        self.boats_dict_copy[e] = [a, b + e]
                                    else:
                                        is_complete = False
                        if is_complete:
                            for e in coord_boats:
                                self.my_map_boats[e[0]][e[1]] = "██"
                            self.boats_dict[num_iter] = self.boats_dict_copy
                            break
                        if w == side ** 4 - 1:
                            no_place = True
                            break
                    if no_place:
                        break
                if no_place:
                    raise Exception("no_place")
            except BaseException:
                sands_error = True
                continue
            sands_error = False
            break

        if map_boats is None:  # если поле не передано, то также делаем поле игроку
            list_2 = copy.deepcopy(self.my_map_boats)
            self.enemy_boats_dict_copy = copy.deepcopy(self.boats_dict)
            self.enemy_boats_dict = copy.deepcopy(self.boats_dict)
            while (time.time() - start_time) < 30:
                try:
                    self.boats = list()
                    if boats is None:
                        boats = [4, 3, 2, 1]
                    for q in range(len(boats[::-1])):
                        self.boats += [len(boats[::-1]) - q] * (boats[::-1][q])
                    self.side = side + 2
                    self.my_map_boats = list()
                    for q in range(self.side):
                        self.my_map_boats.append([None for _ in range(self.side)])
                    self.enemy_map_shots = list()
                    for q in range(self.side):
                        self.enemy_map_shots.append([None for _ in range(self.side)])
                    no_place = False
                    self.boats_dict = dict()
                    num_iter = -1
                    for q in self.boats:
                        num_iter += 1
                        for w in range(side ** 4):
                            a, b = random.randint(0, self.side - 1 - q + 1), random.randint(0, self.side - 1 - q + 1)
                            is_complete = True
                            coord_boats = list()
                            self.boats_dict_copy = dict()
                            if random.random() > 0.5:
                                for e in range(q):
                                    if e == 0:
                                        if a - 1 >= 0 and b - 1 >= 0 and a + 1 < self.side and \
                                                b + 1 <= self.side - 1 and \
                                                self.my_map_boats[a][b] is None and \
                                                self.my_map_boats[a + 1][b] is None and \
                                                self.my_map_boats[a - 1][b] is None and \
                                                self.my_map_boats[a][b + 1] is None and \
                                                self.my_map_boats[a][b - 1] is None and \
                                                self.my_map_boats[a + 1][b + 1] is None and \
                                                self.my_map_boats[a + 1][b - 1] is None and \
                                                self.my_map_boats[a - 1][b + 1] is None and \
                                                self.my_map_boats[a - 1][b - 1] is None:
                                            coord_boats.append([a, b])
                                            self.boats_dict_copy[e] = [a, b]
                                        else:
                                            is_complete = False
                                    else:
                                        if a + e + 1 < self.side and self.my_map_boats[a + e + 1][b] == \
                                                self.my_map_boats[a + e + 1][b - 1] == \
                                                self.my_map_boats[a + e + 1][
                                                    b + 1] is None and a - 1 >= 0 and b - 1 >= 0 and b + e <= self.side - 1:
                                            coord_boats.append([a + e, b])
                                            self.boats_dict_copy[e] = [a + e, b]
                                        else:
                                            is_complete = False
                            else:
                                for e in range(q):
                                    if e == 0:
                                        if a - 1 >= 0 and b - 1 >= 0 and a + 1 < self.side and \
                                                b + 1 <= self.side - 1 and \
                                                self.my_map_boats[a][b] is None and \
                                                self.my_map_boats[a + 1][b] is None and \
                                                self.my_map_boats[a - 1][b] is None and \
                                                self.my_map_boats[a][b + 1] is None and \
                                                self.my_map_boats[a][b - 1] is None and \
                                                self.my_map_boats[a + 1][b + 1] is None and \
                                                self.my_map_boats[a + 1][b - 1] is None and \
                                                self.my_map_boats[a - 1][b + 1] is None and \
                                                self.my_map_boats[a - 1][b - 1] is None:
                                            coord_boats.append([a, b])
                                            self.boats_dict_copy[e] = [a, b]
                                        else:
                                            is_complete = False
                                    else:
                                        if b + e + 1 <= self.side - 1 and self.my_map_boats[a + 1][b + e + 1] == \
                                                self.my_map_boats[a][b + e + 1] == \
                                                self.my_map_boats[a - 1][
                                                    b + e + 1] is None and a - 1 >= 0 and b - 1 >= 0 and a + e < \
                                                self.side:
                                            coord_boats.append([a, b + e])
                                            self.boats_dict_copy[e] = [a, b + e]
                                        else:
                                            is_complete = False
                            if is_complete:
                                for e in coord_boats:
                                    self.my_map_boats[e[0]][e[1]] = "██"
                                self.boats_dict[num_iter] = self.boats_dict_copy
                                break
                            if w == side ** 4 - 1:
                                no_place = True
                                break
                        if no_place:
                            break
                    if no_place:
                        raise Exception("no_place")
                except BaseException:
                    sands_error = True
                    continue
                sands_error = False
                break
            self.enemy_map_boats = copy.deepcopy(list_2)
        else:
            self.enemy_map_boats = map_boats
        if sands_error:  # смотрим ошибки
            self.is_complete = False
        else:
            self.boats_dict_copy = copy.deepcopy(self.boats_dict)
            self.is_complete = True

    def check_complete_map(self):  # метод проверки удачной расстановки кораблей
        if self.is_complete:
            return "complete"
        else:
            return "error"

    def draw(self, my_map=True, map_shots=True):  # метод символьной отрисовки поля
        if (not my_map) and map_shots:
            list_1 = list()
            list_1 = self.enemy_map_shots
        if my_map and (not map_shots):
            list_1 = list()
            list_1 = self.my_map_boats
        if (not my_map) and (not map_shots):
            list_1 = list()
            list_1 = self.enemy_map_boats
        return_str = str()
        return_str += (len(str(len(list_1[1:-1]))) + 1) * " "
        for q in range(self.side - 2):
            if len(str(q + 1)) == 1:
                return_str += str(q + 1)
                return_str += " "
            else:
                return_str += str(q + 1)
        return_str += "\n"
        h = 0
        for q in list_1[1:-1]:
            h += 1
            str_1 = str()
            str_1 = str(h) + " " * (len(str(len(list_1[1:-1]))) - len(str(h))) + "|"
            return_str += str_1
            for w in q[1:-1]:
                if w is None:
                    return_str += "  "
                else:
                    return_str += w
            return_str += "|"
            return_str += "\n"
        return return_str

    def enemy_shot(self, x, y):  # метод вражеского выстрела
        try:
            if not (0 < int(x) <= self.side and 0 < int(y) <= self.side):  # проверяем координаты
                x = 1 / 0
        except BaseException:
            return "input_error"
        x, y, = int(x), int(y)
        if self.my_map_boats[x][y] is None or self.my_map_boats[x][y] == "██":  # если что-то есть или нет, то
            if self.my_map_boats[x][y] is None:
                self.my_map_boats[x][y] = ".."  # если там пусто, то рисуем выстрел и выходим
                self.enemy_map_shots[x][y] = ".."
                return "miss"
            if self.my_map_boats[x][y] == "██":  # если есть корабль
                self.my_map_boats[x][y] = "XX"  # рисуем попадание
                self.enemy_map_shots[x][y] = "XX"
                for q in range(len(self.boats_dict)):  # и идём по словарю с кораблями
                    for w in range(len(self.boats_dict[q])):  # идём по вложенному словарю
                        if self.boats_dict[q][w] == [x, y]:  # когда нашли клетку
                            self.boats_dict[q][w] = None  # делаем её none
                            flag_1 = False  # опускаем флаг
                            for e in range(len(self.boats_dict[q])):  # теперь идём по словарю с нужным кораблём
                                if not self.boats_dict[q][e] is None:  # если хоть одна клетка ещё не none
                                    flag_1 = True  # поднимаем флаг
                            if not flag_1:  # если флаг ввсё еще опущен
                                for r in range(len(self.boats_dict_copy[q])):  # идём по словарю с убитым кораблём
                                    self.my_map_boats[self.boats_dict_copy[q][r][0]][self.boats_dict_copy[q][r][1]] \
                                        = "##"  # рисуем все клетки потопленными
                                    self.enemy_map_shots[self.boats_dict_copy[q][r][0]][self.boats_dict_copy[q][r][1]] \
                                        = "##"  # рисуем все клетки потопленными
                                    for t in self.boats_dict_copy[q]:  # проходим по всем клеткам корабля
                                        for u in [-1, 0, 1]:  # и рисуем выстрелы вокруг
                                            for i in [-1, 0, 1]:
                                                try:
                                                    if self.my_map_boats[self.boats_dict_copy[q][t][0] +
                                                                         u][self.boats_dict_copy[q][t][1] + i] is None:
                                                        self.my_map_boats[self.boats_dict_copy[q][t][0] +
                                                                          u][self.boats_dict_copy[q][t][1] + i] = ".."
                                                        self.enemy_map_shots[self.boats_dict_copy[q][t][0] + u][
                                                            self.boats_dict_copy[q][t][1] + i] = ".."
                                                except BaseException:
                                                    pass
                                # проверяем на выигрыш
                                flag_1 = False  # опускаем флаг
                                for r in range(len(self.boats_dict)):
                                    for t in range(len(self.boats_dict[r])):  # теперь идём по словарю с нужным кораблём
                                        if not self.boats_dict[r][t] is None:  # если хоть одна клетка ещё не none
                                            flag_1 = True  # поднимаем флаг
                                if not flag_1:
                                    return "game_over"  # возвращаем, что игрок выиграл
                                return "kill"  # возврщаем что корабль потоплен
                return "hit"  # возврщаем что в корабль попали
        else:  # если стреляли
            if self.my_map_boats[x][y] == "XX" or self.my_map_boats[x][y] == "##" or self.my_map_boats[x][y] == "..":
                if self.my_map_boats[x][y] == "XX" or self.my_map_boats[x][y] == "##":
                    return "not_shot_already_hit"  # если уже стреляли и попали
                else:
                    return "not_shot_no_ships"  # если пусто

    def get_maps(self, my_map=False, map_shots=False):  # метод получения карты
        if (not my_map) and map_shots:
            list_1 = list()
            for q in self.enemy_map_shots[1:-1]:
                list_1.append(q[1:-1])
            return list_1
        if my_map and (not map_shots):
            list_1 = list()
            for q in self.my_map_boats[1:-1]:
                list_1.append(q[1:-1])
            return list_1
        if (not my_map) and (not map_shots):
            list_1 = list()
            for q in self.enemy_map_boats[1:-1]:
                list_1.append(q[1:-1])
            return list_1

    @property
    def my_shot(self):  # метод выстрела ИИ
        map_chances = [[1 for _ in range(len(self.enemy_map_boats))] for _ in range(len(self.enemy_map_boats))]
        for q in range(len(self.enemy_map_boats)):  # обнуляем выходящие за поле
            for w in range(len(self.enemy_map_boats)):
                if q == 0 or w == 0 or q == len(self.enemy_map_boats) - 1 or w == len(self.enemy_map_boats) - 1:
                    map_chances[q][w] = 0
        for q in range(len(self.enemy_map_boats)):  # если уже потоплено или пусто то ноль
            for w in range(len(self.enemy_map_boats)):
                if self.enemy_map_boats[q][w] == ".." or self.enemy_map_boats[q][w] == "##" or \
                        self.enemy_map_boats[q][w] == "XX":
                    map_chances[q][w] = 0
        for q in range(len(self.enemy_map_boats)):  # ищем подстреленные корабли
            for w in range(len(self.enemy_map_boats)):
                if self.enemy_map_boats[q][w] == "XX":  # домножаем на квадрат поля, чтобы точно было больше
                    map_chances[q + 1][w + 1] = 0  # но сначала обнуляем диагональные клетки
                    map_chances[q + 1][w - 1] = 0
                    map_chances[q - 1][w + 1] = 0
                    map_chances[q - 1][w - 1] = 0
                    if self.enemy_map_boats[q][w + 1] is None or self.enemy_map_boats[q][w + 1] == "██":
                        map_chances[q][w + 1] *= (len(self.enemy_map_boats) ** 2 + 4)
                    if self.enemy_map_boats[q + 1][w] is None or self.enemy_map_boats[q + 1][w] == "██":
                        map_chances[q + 1][w] *= (len(self.enemy_map_boats) ** 2 + 4)
                    if self.enemy_map_boats[q][w - 1] is None or self.enemy_map_boats[q][w - 1] == "██":
                        map_chances[q][w - 1] *= (len(self.enemy_map_boats) ** 2 + 4)
                    if self.enemy_map_boats[q - 1][w] is None or self.enemy_map_boats[q - 1][w] == "██":
                        map_chances[q - 1][w] *= (len(self.enemy_map_boats) ** 2 + 4)
        for w in range(len(self.enemy_map_boats)):  # и опять по полю
            for e in range(len(self.enemy_map_boats)):
                if not (self.enemy_map_boats[w][e] is None or self.enemy_map_boats[w][e] == "██"):
                    continue
                for q in self.boats:  # идём по кораблям
                    flag_miss = False  # делаем флаг
                    for r in range(q):  # идём по кораблю и вправо
                        try:
                            if not (self.enemy_map_boats[w][e + r] is None or self.enemy_map_boats[w][e + r] == "██"):
                                flag_miss = True
                                break
                        except:
                            flag_miss = True
                            break
                    if not flag_miss:
                        if map_chances[w][e] != 0:
                            map_chances[w][e] += 1
                    # то же самое
                    flag_miss = False  # делаем флаг
                    for r in range(q):  # идём по кораблю и вправо
                        try:
                            if not (self.enemy_map_boats[w + r][e] is None or self.enemy_map_boats[w + r][e] == "██"):
                                flag_miss = True
                                break
                        except:
                            flag_miss = True
                            break
                    if not flag_miss:
                        if map_chances[w][e] != 0:
                            map_chances[w][e] += 1
                    revers_copy = copy.deepcopy(self.enemy_map_boats)
                    revers_copy_1 = list()
                    for r in revers_copy[::-1]:
                        revers_copy_1.append(r[::-1])
                    # то же самое но наоборот
                    flag_miss = False  # делаем флаг
                    for r in range(q):  # идём по кораблю и вправо
                        try:
                            if not (revers_copy_1[w][e + r] is None or revers_copy_1[w][e + r] == "██"):
                                flag_miss = True
                                break
                        except:
                            flag_miss = True
                            break
                    if not flag_miss:
                        if map_chances[len(self.enemy_map_boats) - 1 - w][len(self.enemy_map_boats) - 1 - e] != 0:
                            map_chances[len(self.enemy_map_boats) - 1 - w][len(self.enemy_map_boats) - 1 - e] += 1
                    # то же самое
                    flag_miss = False  # делаем флаг
                    for r in range(q):  # идём по кораблю и вправо
                        try:
                            if not (revers_copy_1[w + r][e] is None or revers_copy_1[w + r][e] == "██"):
                                flag_miss = True
                                break
                        except:
                            flag_miss = True
                            break
                    if not flag_miss:
                        if map_chances[len(self.enemy_map_boats) - 1 - w][len(self.enemy_map_boats) - 1 - e] != 0:
                            map_chances[len(self.enemy_map_boats) - 1 - w][len(self.enemy_map_boats) - 1 - e] += 1

        max_x = 0
        max_y = 0
        max_list = list()
        for q in map_chances:
            max_list.append(max(q))
        max_x = max_list.index(max(max_list))
        max_y = map_chances[max_x].index(max(map_chances[max_x]))
        x, y = max_x, max_y
        self.last_my_shot = [x, y]  # записываем выстрел

        for eee in map_chances:
            d = list()
            for e in eee:
                d.append(str(e))
            print("\t".join(d))
        # дальше перерисовка полей
        if self.enemy_map_boats[x][y] is None or self.enemy_map_boats[x][y] == "██":  # если что-то есть или нет, то
            if self.enemy_map_boats[x][y] is None:
                self.enemy_map_boats[x][y] = ".."  # если там пусто, то рисуем выстрел и выходим
                return "miss"
            if self.enemy_map_boats[x][y] == "██":  # если есть корабль
                self.enemy_map_boats[x][y] = "XX"  # рисуем попадание
                for q in range(len(self.enemy_boats_dict)):  # и идём по словарю с кораблями
                    for w in range(len(self.enemy_boats_dict[q])):  # идём по вложенному словарю
                        if self.enemy_boats_dict[q][w] == [x, y]:  # когда нашли клетку
                            self.enemy_boats_dict[q][w] = None  # делаем её none
                            flag_1 = False  # опускаем флаг
                            for e in range(len(self.enemy_boats_dict[q])):  # теперь идём по словарю с нужным кораблём
                                if not self.enemy_boats_dict[q][e] is None:  # если хоть одна клетка ещё не none
                                    flag_1 = True  # поднимаем флаг
                            if not flag_1:  # если флаг ввсё еще опущен
                                for r in range(len(self.enemy_boats_dict_copy[q])):  # идём по словарю с убитым кораблём
                                    self.enemy_map_boats[self.enemy_boats_dict_copy[q][r][0]][
                                        self.enemy_boats_dict_copy[q][r][1]] \
                                        = "##"  # рисуем все клетки потопленными
                                    for t in self.enemy_boats_dict_copy[q]:  # проходим по всем клеткам корабля
                                        for u in [-1, 0, 1]:  # и рисуем выстрелы вокруг
                                            for i in [-1, 0, 1]:
                                                try:
                                                    if self.enemy_map_boats[self.enemy_boats_dict_copy[q][t][0] +
                                                                            u][self.enemy_boats_dict_copy[q][t][1] +
                                                                               i] is None:
                                                        self.enemy_map_boats[self.enemy_boats_dict_copy[q][t][0] + u][
                                                            self.enemy_boats_dict_copy[q][t][1] + i] = ".."
                                                except BaseException:
                                                    pass
                                # проверяем на выигрыш
                                flag_1 = False  # опускаем флаг
                                for r in range(len(self.enemy_boats_dict)):
                                    for t in range(len(self.enemy_boats_dict[r])):
                                        # теперь идём по словарю с нужным кораблём
                                        if not self.enemy_boats_dict[r][t] is None:  # если хоть одна клетка ещё не none
                                            flag_1 = True  # поднимаем флаг
                                if not flag_1:
                                    return "game_over"  # возвращаем, что игрок выиграл
                                return "kill"  # возврщаем что корабль потоплен
                return "hit"  # возврщаем что в корабль попали
        else:  # если стреляли
            if self.enemy_map_boats[x][y] == "XX" or self.enemy_map_boats[x][y] == "##" or \
                    self.enemy_map_boats[x][y] == "..":
                if self.enemy_map_boats[x][y] == "XX" or self.enemy_map_boats[x][y] == "##":
                    return "not_shot_already_hit"  # если уже стреляли и попали
                else:
                    return "not_shot_no_ships"  # если пусто

    def get_last_my_shot(self):
        return self.last_my_shot

    @staticmethod
    def help():
        print("Методы:")
        print("check_complete_map - проверка на расстановку кораблей")
        print("\tвозвращаемые значения: complete, error")

        print("draw - отрисовка карты")
        print("\tаргументы: my_map (чья карта), map_shots (карта выстрелов или кораблей)")
        print("\tвозвращаемые значения: [карта кораблей в виде таблицы]")

        print("enemy_shot - вражеский выстрел")
        print("\tаргументы: x, y (координаты от 1 до ширины поля из верхнего левого угла)")
        print("\tвозвращаемые значения: input_error, miss (промах), game_over (игра закончена победой игрока), kill "
              "(корабль убит), hit (в корабль попали), not_shot_already_hit(в этой клетке корабль, уже стреляли), "
              "not_shot_no_ships (уже стреляли, но клетка пустая)")

        print("get_maps - получить карту")
        print("\tаргументы: аналогичны методу draw")
        print("\tвозвращаемые значения: [карта кораблей в виде таблицы]")

        print("my_shot - выстрел ИИ")
        print("\tвозвращаемые значения: аналогичны методу enemy_shot, кроме game_over, (игра закончена победой ИИ)")