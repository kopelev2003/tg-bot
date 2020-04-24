from bs4 import BeautifulSoup
import requests


def currency_checker():
    def dollar_checker():
        catalog = []
        dollar_link = "https://minfin.com.ua/currency/nbu/"
        page_response = requests.get(dollar_link, timeout=5)
        page_content = BeautifulSoup(page_response.content, "html.parser")
        tbody = page_content.find("tbody")
        trs = tbody.find_all("tr")

        table_bel = page_content.find("table", attrs={"class": "mfm-responsive-table mfm-table mfcur-table-lg mfcur-table-lg-nbu"})
        thead_bel = table_bel.find_next("thead", attrs={"class": "responsive-hide"})
        tbody_bel = thead_bel.find_next("tbody")
        tr_bel = tbody_bel.find_all_next("tr", attrs={"class": "row--collapse"})[3]
        td_bel = tr_bel.find("td", attrs={"class": "responsive-hide td-collapsed mfm-text-nowrap mfm-text-right"})
        for tr in trs:
            td = tr.find("td", attrs={"class": "responsive-hide td-collapsed mfm-text-nowrap mfm-text-right"})
            catalog.append(td.text)
        catalog.append(td_bel.text)
        return catalog


    x = int(0)
    currency = dollar_checker()
    currency_lists = " ".join(currency).split("\n")



    for currency_list in currency_lists:
        if currency_list == " ":
            currency_lists.remove(currency_list)
        if currency_list == "":
            currency_lists.remove(currency_list)

    currency_lists = currency_lists[::2]
    names = ["ДОЛЛАР: ", "ЕВРО: ", "РУБЛЬ: ", "ПОЛЬСКИЙ ЗЛОТЫЙ: ", "ШВЕЙЦАРСКИЙ ФРАНК: ", "АНГЛИЙСКИЙ ФУНТ СТЕРЛИНГОВ: ", "БЕЛОРУССКИЙ РУБЛЬ: "]
    for name in names:
        # print(name, currency_lists[x])
        x += 1
    return currency_lists






















