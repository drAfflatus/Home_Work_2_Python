from unicodedata import digit
import os
# Функция читает файл с рецептами. Возвращает сложный словарь с содержимым файла. Аргумент функции-имя файла с рецептом
def file_to_dict(name_file):
    with open('recipes.txt',encoding='utf-8') as fr:
        cook_book = dict()
        data_ingr = list()
        name_dish = ''
        for line in fr:
            vol_line = line.strip()
            if vol_line.isdigit():
                ##print(vol_line) # количество позиций ингридиентов в блюде . Оно нам нужно ? Неа ... поехали дальше
                pass
            elif vol_line.find('|')!=-1:   # есть разделитель , значит строка с ингридиентом . парсим ее
                str_ingr = vol_line.split(sep='|')
                data_ingr += [{'ingredient_name': str_ingr[0], 'quantity': int(str_ingr[1]),'measure': str_ingr[2]}]
            elif vol_line == '': # пустая строчка  , блюдо кончилось , впереди новое или конец файла
                cook_book[name_dish] = data_ingr.copy()
                data_ingr = []  # обнуляем накопитель ингридиентов для блюда
            else:
                name_dish =vol_line
    return cook_book

def get_shop_list_by_dishes(dishes, person_count):

    result = {}
    if  type(dishes) is list:
        dict_book =file_to_dict('recipes.txt') # читаем из файла в словарь
        for nn,dish in enumerate(dishes):
            #print(dish)
            ingr = dict_book.get(dish)
            if ingr!= None:
                for i,ing_ in enumerate(ingr):
                    #print(ing_)
                    if result.get(ing_['ingredient_name'])!=None: # проверяем был ли этот ингр. уже ранее подсчитан.
                                                                  # если да то прибавляем при перезаписи словаря
                       double_ingr = result.get(ing_['ingredient_name']).get('quantity')
                    else:
                        double_ingr = 0  # обнуляем счетчик прежнего использования ингр( если он был, конечно)
                    result.update({ing_['ingredient_name']:{'measure':ing_['measure'],
                                                            'quantity':ing_['quantity']*person_count+double_ingr}})

    else:
        print('Ошибка . перечень блюд нужно передавать в функцию в списке ')

    sorted_items = sorted(result.items())  # сортируем выходной словарь, сначала в список , потом в словарь
    sorted_dict = dict(sorted_items)
    return sorted_dict


# Функция сканирует текущую директорию, выбирает в список файлы удовлетворяющие паттерну расширения напр '.txt'
# игнорируя целевой файл заполнения , если он был создан ранее и не нулевой
def scan_files(pattern,file_target):
    files = []
    file_path = os.getcwd()
    for filename in os.listdir(file_path):
        if filename.endswith(pattern) and (filename != file_target):
            iter_f=os.path.join(file_path, filename)
            files.append(iter_f)
    return files

# функция обрабатывает файлы из текущей папки , сохраняя содержимое файлов в целевом файле согласно
# ранжированию задания.  pattern - шаблон паттерна расширения для отбора файлов (".<ext>")
# file_target - имя файла для итогового сохранения результатов ранжирования
def merge_files(pattern,file_target):
    l_files=scan_files(pattern,file_target)
    if not(len(l_files)):
        return print('Файлов для слияния нет. Операция не выполнена')
    sum_list = []
    for it in l_files:
        with open(it,encoding='utf-8') as f:
            list1 = f.readlines()
            list1.insert(0, str(len(list1))+'\n')
            list1.insert(0, f.name+'\n')
            if list1[-1][-1]!='\n':
                list1.append('\n')
        sum_list.append(list1)

    tmp=sorted(sum_list,key=len)
    summary_text = []
    i=0
    while i<len(l_files):
        summary_text.extend(tmp[i])
        i+=1
    with open(file_target,'w',encoding='utf-8') as f:
        f.writelines(summary_text)
    return

# 1 задание
print(f'прочли из файла в словарь\n {file_to_dict("recipes.txt")}')

# 2 задание
print(f'ингридиенты по блюдам\n{get_shop_list_by_dishes(["Запеченный картофель","Омлет"], 2)}')

# 3 задание

merge_files(".txt",'added_text.txt')
