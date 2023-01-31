import os.path

import xlsxwriter
import random


class Result:
    """
    Класс для представления результата.
    ...
    Attributes
    ----------
    res_and_lists : tuple
        res - словарь(ключ - версия регулярного выражения, значение - список найденных фраз после прогона)
        list_of_strings - список фраз, считанных из файла(ов)
        list_regulars - словарь(ключ - версия регулярного выражения, значение - регулярное выражение)
        mark - строка(маркер регулярного выражения)
    Methods
    -------
    create_result_xlsx():
        Создание результирующей таблицы, где отражено, в каких фразах есть различия по версиям
    """

    def __init__(self, res_and_lists):
        self.list_of_strings = res_and_lists[1]
        self.res = res_and_lists[0]
        self.list_regulars = res_and_lists[2]
        self.marker = res_and_lists[3]

    def get_res(self):
        return self.res

    def get_list_of_strings(self):
        return self.list_of_strings

    def create_result_xlsx(self):
        """
        Создаёт результирующую таблицу, в которой отражено, в каких фразах есть различия по версиям
        -------
        Return:
            namefile - имя файла
        """

        namefile = f'{self.marker}{random.randint(1, 1000)}.xlsx'
        while os.path.exists(namefile):
            namefile = f'{self.marker}{random.randint(1, 1000)}.xlsx'

        workbook = xlsxwriter.Workbook(namefile)
        worksheet = workbook.add_worksheet()

        row = 2
        for string in self.list_of_strings:
            if string != '\n':
                worksheet.write(row, 0, string)
                row += 1

        column = 1
        for version, value in sorted(self.res.items()):
            reg = self.list_regulars[version]
            worksheet.write(0, column, reg)
            worksheet.write(1, column, version)
            row = 2
            for i in value:
                for string in self.list_of_strings:
                    if string != '\n':
                        if i == string:
                            worksheet.write(row, column, '+')
                            row = 2
                            break
                        else:
                            row += 1
            column += 1

        workbook.close()
        return namefile
