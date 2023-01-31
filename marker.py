from data import db_session
from data.regular_table import RegularTable
from reader import Reader
import regex


class Marker:
    """
    Класс для представления маркера регулярного выражения.
    ...
    Attributes
    ----------
    namefile : str
        название файла
    Methods
    -------
    take_regulars_expressions():
        Парсит регулярные выражения
    get_data():
        Производит прогон регулярных выражений по фразам
    """

    def __init__(self, namefile):
        self.session = db_session.create_session()
        self.namefile = namefile
        self.regulars_expressions = []

    def take_regulars_expressions(self):
        """
        Парсит регулярные выражения
        """

        regulars = {'tg': 'Реклама тг-каналов', 'course': 'Реклама курсов',
                    'markets': 'Реклама товаров на маркетплейсах'}
        mark = self.namefile.split('_')[1].split('.')[0]
        for i in self.session.query(RegularTable).filter(RegularTable.marker == regulars[mark]).all():
            self.regulars_expressions.append(i.regular_expression)

    def get_regulars_expressions(self):
        return self.regulars_expressions

    def get_data(self):
        """
        Производит прогон регулярных выражений по фразам
        -------
        Return:
            res - словарь(ключ - версия регулярного выражения, значение - список найденных фраз после прогона)
            list_of_strings - список фраз, считанных из файла(ов)
            list_regulars - словарь(ключ - версия регулярного выражения, значение - регулярное выражение)
            mark - строка(маркер регулярного выражения)
        """

        reader = Reader(self.namefile)
        list_regulars = {}
        res = {}
        list_of_strings = reader.read()
        for reg_exp in self.regulars_expressions:
            regx = regex.compile(reg_exp)
            version = str(
                self.session.query(RegularTable).filter(RegularTable.regular_expression == reg_exp).first().version)
            list_regulars[version] = reg_exp
            res[version] = []
            for string in list_of_strings:
                lst = regex.findall(regx, string)
                if lst:
                    res[version].append(string)

        return res, list_of_strings, list_regulars, reader.mark
