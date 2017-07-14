# -*- coding: utf-8 -*-


class Months():
    months = {
        'gener': '01',
        'febrer': '02',
        'març': '03',
        'abril': '04',
        'maig': '05',
        'juny': '06',
        'juliol': '07',
        'agost': '08',
        'setembre': '09',
        'octubre': '10',
        'novembre': '11',
        'desembre': '12',
    }

    @staticmethod
    def get_month_number(month_text):
        """
        Return number of month depends on month_text given by parameter
        :param month_text: String
        :return: String
        """
        return Months.months.get(month_text, None)
