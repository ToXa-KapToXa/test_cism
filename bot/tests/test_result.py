import unittest
import pyexcel
from bot.result_xlsx import Result


class TestResult(unittest.TestCase):
    def setUp(self):
        a = (
            {
                '1.0': ['Платный курс', 'Бесплатный курс'],
                '1.1': ['Платный курс', 'Бесплатный курс', 'Бесплатный миникурс по Adobe Illustrator.'],
                '3.0': ['Платный курс', 'Бесплатный курс', '10 бесплатных онлайн-курсов по психологии',
                        'Бесплатный миникурс по Adobe Illustrator.']
            },
            ['Платный курс', 'Бесплатный курс', '10 бесплатных онлайн-курсов по психологии',
             'Бесплатный миникурс по Adobe Illustrator.'],
            {
                '1.0': r'(?i)(?:бес)?платн(?:ые|ый|ых)\sкурс(?:ы|ов|ам|а)?|курс(?:е|ах)?\s«[\w\-_0-9]*»',
                '1.1': r'(?i)(?:бес)?платн(?:ые|ый|ых)\s(?:мини)?курс(?:ы|ов|ам|а)?|(?:мини)?курс(?:е|ах)?\s«[\w\-_0-9]*»',
                '3.0': r'(?i)(?:бес)?платн(?:ые|ый|ых)\s(?:мини)?курс(?:ы|ов|ам|а)?|(?:мини)?курс(?:е|ах)?\s«[\w\-_0-9]*»|доступ\s[\s\w]*(?:мини)?курс(?:ы|ов|ам|а|у)?|курс(?:ы|ов|ам|а)?\s(?:по\sссылке)|подар(?:ить|ок)\sкурс(?:ы|ов)?|(?:мини)?курс[ы]?\s(?:про|по)|онлайн-курс(?:ы|ов|ам|а)?'
            },
            'testDataset'
        )
        self.result = Result(a)

    def test_result(self):
        test = []
        strings = pyexcel.get_array(file_name=r'result_test.xlsx')
        for string in strings:
            for j in string:
                test.append(j)

        result = []
        strings = pyexcel.get_array(file_name=f'{self.result.create_result_xlsx()}')
        for string in strings:
            for j in string:
                result.append(j)
        self.assertEqual(result, test)


if __name__ == '__main__':
    unittest.main()
