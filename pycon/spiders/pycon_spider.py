



import re

import scrapy
from scrapy import Selector

from ..Months import Months

from ..items import PyconItem


class PyconSpider(scrapy.Spider):
    name = "pycon"
    start_urls = [
        'https://2017.es.pycon.org/ca/schedule/',
    ]

    # Xpaths
    container_xpath = '//div[contains(@class, "schedule")]/div'
    date_xpath = './div[contains(@class, "day")]'
    slot_xpath = './div[contains(@class, "slot-intermediate") or contains(@class, "slot-basic") or contains(@class, "slot-advanced")]'

    # Xpath inside slot
    slot_level_xpath = './@class'
    inner_xpath = './/div[@class="slot-inner"]'
    slot_id_xpath = inner_xpath + '/@data-slot'
    slot_hour_xpath = inner_xpath + '/strong/text()'
    slot_type_xpath = inner_xpath + '/span[@class="slot-kind"]/text()'
    slot_title_xpath = inner_xpath + '/h3/a/text()'
    slot_url_xpath = inner_xpath + '/h3/a/@href'
    slot_language_xpath = inner_xpath + '/h3/a/small/text()'
    slot_speakers_xpath = inner_xpath + '/p/strong/text()'
    slot_room_xpath = inner_xpath + '/p[contains(@class, "default-room")]/text()'
    slot_description_xpath = '//div[@id="slot-description-{}"]//p/text()'


    def __init__(self, tor=None, *args, **kwargs):
        super(PyconSpider, self).__init__(*args, **kwargs)
        self.tor = tor
        """
        import sys
        sys.path.append('/home/jordi/opt/scrapy_pycon/pycharm-debug.egg')
        import pydevd
        pydevd.settrace('localhost', port=7502, stdoutToServer=True, stderrToServer=True)
        """
    def parse(self, response):
        sel = Selector(response)
        divs_schedule = sel.xpath(self.container_xpath)

        items = []
        slot_date = ''
        for div_schedule in divs_schedule:
            # Check if current div is a "date div" and get the date
            if self.is_date(div_schedule):
                slot_date = self.get_date(div_schedule)

            # Check if current div is a slot and get their data
            if self.is_slot(div_schedule):
                for slot in div_schedule.xpath(self.slot_xpath):
                    items.append(self.get_slot(slot, slot_date))

        return items


    def is_date(self, sel):
        """
        If given selector is a date return True.
        :param sel: Selector
        :return: Boolean
        """
        return True if sel.xpath(self.date_xpath) else False

    def is_slot(self, sel):
        """

        :param sel: Selector
        :return: Boolean
        """
        return True if sel.xpath(self.slot_xpath) else False

    def get_date(self, sel):
        """
        Return string with date from selector
        :param sel: Selector
        :return: String
        """
        date = sel.xpath(self.date_xpath + '/h2/text()')
        if date:
            date_str = date.extract_first()
            # Transform text date to iso date (YYYY-MM-DD)
            date_re = re.search('(?P<day>\d{2}) de (?P<month>\w+) de (?P<year>\d{4})', date_str)
            if date_re:
                day = date_re.group('day')
                month_str = date_re.group('month')
                year = date_re.group('year')
                month = Months.get_month_number(month_str)
                return '{}-{}-{}'.format(year, month, day)
        raise Exception("The date can't be gotten")

    def get_slot(self, sel, date):
        """

        :param sel: Selector
        :param date: String
        :return: PyconItem
        """
        item = PyconItem()

        item['level'] = self.get_level(sel)
        item['id'] = sel.xpath(self.slot_id_xpath).extract_first()
        item['hour'] = sel.xpath(self.slot_hour_xpath).extract_first()
        item['type'] = sel.xpath(self.slot_type_xpath).extract_first()
        item['title'] = sel.xpath(self.slot_title_xpath).extract_first().strip()
        item['lang'] = sel.xpath(self.slot_language_xpath).extract_first().strip()
        item['speakers'] = sel.xpath(self.slot_speakers_xpath).extract_first().strip()
        item['room'] = sel.xpath(self.slot_room_xpath).extract_first().strip()
        item['description'] = sel.xpath(self.slot_description_xpath.format(item['id'])).extract_first().strip()
        item['date'] = date

        """
        slot_url = sel.xpath(self.slot_room_xpath).extract_first().strip()
        if slot_url is not None:
            next_page = response.urljoin(slot_url)
            yield scrapy.Request(next_page, callback=self.parse_slot_detail)
        """

        return item

    def get_level(self, sel):
        """

        :param sel: Selector
        :return:
        """
        slot_class = sel.xpath(self.slot_level_xpath)
        if 'basic' in slot_class:
            return 'basic'
        elif 'intermediate' in slot_class:
            return 'intermediate'
        else:
            return 'advanced'

    # def parse_slot_detail(self, response):