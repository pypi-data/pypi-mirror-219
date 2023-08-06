from datetime import datetime

import re

import unittest

import logging

from cache import MemoryCache

from krx import KrxKindWeb, parse_corp_list

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s [%(levelname)s] %(message)s')
logger = logging.getLogger("krx_api")
logger.setLevel(logging.DEBUG)

class TestKrxKindWebSearch(unittest.TestCase):
    def test_list_search(self):
        web = KrxKindWeb(cache=MemoryCache())
        dt = datetime.strptime("20230623", "%Y%m%d")
        items = web.fetch_list_search(keyword="단기과열종목", from_dt=dt, to_dt=dt, time_sleep=0.5)

        print(items)

    def test_list_search_range(self):
        web = KrxKindWeb(cache=MemoryCache())
        from_dt = datetime.strptime("20230612", "%Y%m%d")
        to_dt = datetime.strptime("20230712", "%Y%m%d")
        items = web.fetch_list_search(keyword="단기과열종목", from_dt=from_dt, to_dt=to_dt, time_sleep=0.5)

        logger.info(f"item count : {len(items)}")
        for item in items:
            logger.info(item)

    def test_document_link(self):
        web = KrxKindWeb(cache=MemoryCache())
        links = web.get_document_link("20230310000434")
        print(links)

    def test_corp_list(self):
        web = KrxKindWeb(cache=MemoryCache())
        soup = web._corp_list()

        table = soup.find("table")
        tbody = table.find("tbody")
        trs = tbody.select("tr")
        for tr in trs:
            tds = tr.select("td")
            company = tds[0].text.strip()
            market = tds[0].find("img")["alt"]
            onclick = tds[0].find("a")["onclick"]

            match = re.search(r"\('(\d+)'\)", onclick)
            code = match.group(1) if match else None
            kind = tds[1].text.strip()
            major_product = tds[2].text.strip()
            listing_date = tds[3].text.strip()
            finclosing_month = tds[4].text.strip()
            ceo = tds[5].text.strip()
            location = tds[7].text.strip()
            print(f"company : {company}, market : {market}, code : {code}, kind : {kind}, major_product : {major_product}, "
                  f"listing_date : {listing_date}, finclosing_month : {finclosing_month}, ceo : {ceo}, location : {location}")

        paging_section = soup.select("section.paging-group")[0]
        total_count = int(paging_section.select("em")[0].text.replace(",", ""))
        section_text = paging_section.text
        total_row = list(filter(lambda x: "전체" in x.strip(), section_text.split("\n")))[0]
        current_per_total = total_row.split(":")[-1].strip()
        current_page, total_page = map(lambda x: int(x.strip()), current_per_total.split("/"))
        print(f"total : {total_count}, pages : {current_page}/{total_page}")


    def test_corp_list_all(self):
        web = KrxKindWeb(cache=MemoryCache())
        all_corps = web.corp_list()

        for corp in all_corps:
            print(corp)