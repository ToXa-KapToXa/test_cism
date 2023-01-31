import unittest
from reader import Reader


class TestReader(unittest.TestCase):
    def setUp(self):
        self.reader_xlsx = Reader(r'test_testDataset.xlsx')
        self.reader_txt = Reader(r'test_testDataset.txt')
        self.reader_zip = Reader(r'test_testDataset.zip')
        self.reader_tar = Reader(r'test_testDataset.tar.gz')
        self.reader_csv = Reader(r'test_testDataset.csv')
        self.read = ['Платный курс', 'Бесплатный курс', '10 бесплатных онлайн-курсов по психологии',
                     'Бесплатный миникурс по Adobe Illustrator.']

    def test_xlsx(self):
        self.assertEqual(self.reader_xlsx.read(), self.read)

    def test_txt(self):
        self.assertEqual(self.reader_txt.read(), self.read)

    def test_tar(self):
        self.assertEqual(self.reader_tar.read(), self.read)

    def test_zip(self):
        self.assertEqual(self.reader_zip.read(), self.read)

    def test_csv(self):
        self.assertEqual(self.reader_csv.read(), self.read)


if __name__ == '__main__':
    unittest.main()