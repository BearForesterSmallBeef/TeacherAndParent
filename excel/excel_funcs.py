import os
import pandas

HEADER_LIST = ["login", "password", "name", "surename", "class", "middlename"]


class ExcelErrors:
    ERRORS_DICT = {
        0: "Учетная запись родителя успешно созданна",
        1: "Что-то пошло не так при открытии файла",
        2: "Данный файл не соответствует шаблону",
        3: "Что-то пошло не так при чтение файла",
        4: "Что-то пошло не так при создании родителей",
        5: "Не достаточно данных для создания родителя",
        6: "Указанного класса не существует",
        7: "Что-то пошло не так при создание учетной записи",
        8: "Указанные логин и/или пароль не соответствует(ют) требованиям - длинна не менее 10 символов",
        9: "Что-то пошло не так при записи в конечный файл",
        10: "Все прошло успешно!",
        11: "Пользователь с таким логином уже существует"
    }

    def __init__(self, number, add=""):
        self.number = number
        self.message = self.ERRORS_DICT[number] + add

    def __repr__(self):
        return self.message

    def __str__(self):
        return self.message


def read_excel(excel_file):
    try:
        import pandas
        pandas.set_option('display.max_rows', None)
        pandas.set_option('display.max_columns', None)
        file = pandas.read_excel(excel_file)
        file = file.fillna("")
        return file
    except Exception as ex:
        print(ex)
        return ExcelErrors(1)


def excel_parse(excel_file):
    file = read_excel(excel_file)
    if isinstance(file, ExcelErrors):
        return file
    for i in HEADER_LIST:
        if i not in list(dict(file).keys()):
            return ExcelErrors(2)
    try:
        register_list = []
        length = len(file[HEADER_LIST[0]])
        for i in range(length):
            reg_dict = {}
            for j in HEADER_LIST:
                reg_dict[j] = file[j][i]
            register_list.append(reg_dict)
        return register_list
    except Exception as ex:
        print(ex)
        return ExcelErrors(3)


def create_parents(excel_file):
    register_list = excel_parse(excel_file)
    if isinstance(register_list, ExcelErrors):
        return register_list
    from app.auth.views import create_parent
    try:
        for i in register_list:
            lost = []
            for j in i.keys():
                if j != "middlename" and i[j] == "":
                    lost.append(i)
            if lost:
                i["report"] = ExcelErrors(5, " " + ", ".join(map(str(lost))))
                continue
            try:
                i["report"] = ExcelErrors(create_parent(*[i[h] for h in HEADER_LIST])).message
            except Exception as ex:
                print(ex)
    except Exception as ex:
        print(ex)
        return ExcelErrors(4)
    return register_list


def data_parent_registration(excel_file, way):
    register_list = create_parents(excel_file)
    if isinstance(register_list, ExcelErrors):
        return register_list
    try:
        if not os.access("excel\\reports", os.F_OK):
            os.mkdir("excel\\reports")

        os.mkdir("excel\\reports\\" + way)

        output_file_name = way + ".xlsx"
        file = open("excel\\reports\\" + way + "\\" + output_file_name, "w")
        file.close()

        output_dataframe = pandas.DataFrame([[i for i in register_list[0].keys() if i != "password"]] +
                                            [[i[j] for j in [i for i in register_list[0].keys() if i != "password"]]
                                             for i in register_list])
        output_dataframe.to_excel("excel\\reports\\" + way + "\\" + output_file_name)
        return ExcelErrors(10)
    except Exception as ex:
        print(ex)
        return ExcelErrors(9)
