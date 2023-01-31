from zipfile import ZipFile
from tarfile import TarFile
import pyexcel
import os
import csv


class Reader:
    """
    Класс для чтения файлов разных форматов.
    ...
    Attributes
    ----------
    namefile : str
        название файла
    Methods
    -------
    read():
        По расширению файла определяет метод для чтения файла
    read_txt():
        Чтение txt-файла
    read_zip():
        Чтение zip-архива
    read_tar():
        Чтение tar-архива
    read_xlsx():
        Чтение excel таблицы
    read_csv():
        Чтение csv таблицы
    """

    def __init__(self, namefile):
        self.namefile = namefile
        self.expansion = namefile.split('_')[1].split('.')[-1]
        self.mark = namefile.split('_')[1].split('.')[0]

    def read(self):
        """
        По расширению файла определяет метод для чтения файла
        -------
        Return:
            read_strings - список фраз, считанных из файла(ов)
        """

        if self.expansion == 'txt':
            read_strings = self.read_txt()
        elif self.expansion == 'zip':
            read_strings = self.read_zip()
        elif self.expansion == 'gz':
            read_strings = self.read_tar()
        elif self.expansion == 'xlsx':
            read_strings = self.read_xlsx()
        elif self.expansion == 'csv':
            read_strings = self.read_csv()
        return read_strings

    def read_txt(self):
        """
        Чтение txt-файла
        -------
        Return:
            read_strings - список фраз, считанных из файла(ов)
        """

        with open(f'datasets/{self.mark}/{self.namefile}', encoding='utf-8') as file:
            read = file.readlines()
            read_res = []
            for i in read:
                i = i.replace('\n', '')
                if i and i != ' ':
                    read_res.append(i)
        return read_res

    def read_zip(self):
        """
        Чтение zip-архива
        -------
        Return:
            read_strings - список фраз, считанных из файла(ов)
        """

        read = []
        with ZipFile(f'datasets/{self.mark}/{self.namefile}', 'r') as zipp:
            for item in zipp.infolist():
                if item.filename.split('.')[-1] == 'txt':
                    with zipp.open(item.filename, mode='r') as file:
                        read_file = list(map(lambda x: x.decode('utf-8'), file.readlines()))
                        for i in read_file:
                            i = i.replace('\r\n', '')
                            if i and i != ' ':
                                read.append(i)
        return read

    def read_tar(self):
        """
        Чтение tar-архива
        -------
        Return:
            read_strings - список фраз, считанных из файла(ов)
        """

        read = []
        with TarFile.open(f'datasets/{self.mark}/{self.namefile}', 'r') as tar:
            tar.extractall(path='tarfiles')
        files = os.listdir('tarfiles')
        for file in files:
            if file.endswith('txt'):
                with open(rf'tarfiles/{file}', encoding='utf-8') as f:
                    strings = f.readlines()
                    for i in strings:
                        i = i.replace('\n', '')
                        if i and i != ' ':
                            read.append(i)
            os.remove(rf'tarfiles/{file}')
        return read

    def read_xlsx(self):
        """
        Чтение excel таблицы
        -------
        Return:
            read_strings - список фраз, считанных из файла(ов)
        """

        read = []
        strings = pyexcel.get_array(file_name=f'datasets/{self.mark}/{self.namefile}')
        for string in strings:
            for j in string:
                if j and j != ' ' and j != '\n':
                    read.append(j)
        return read

    def read_csv(self):
        """
        Чтение csv таблицы
        -------
        Return:
            read_strings - список фраз, считанных из файла(ов)
        """

        read = []
        flag = True
        for row in csv.reader(open(f'datasets/{self.mark}/{self.namefile}', encoding='utf-8'), delimiter=';'):
            for i in row:
                if flag:
                    a = i[1:]
                    flag = False
                else:
                    a = i
                if a and a != ' ' and a != '\n':
                    read.append(a)

        return read
