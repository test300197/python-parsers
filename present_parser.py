import requests
from bs4 import BeautifulSoup
from pprint import pprint
from re import compile
from datetime import datetime


def get_html(url):
    req = requests.get(url)
    return req.text


def main(url):
    html_code = get_html(url)

    data = {
        'sourceMedia': None,
        'sourceUrl': None,
        'addDate': None,
        'address': None,
        'offerTypeCode': None,
        'categoryCode': None,
        'buildingType': None,
        'buildingClass': None,
        'typeCode': None,
        'phones_import': None,
        # 'owner_phones': None
    }

    global soup
    global breadcrumbs
    soup = BeautifulSoup(html_code, 'lxml')

    tag_breadcrumbs = soup.find('div', class_='breadcrumbs')
    breadcrumbs = tag_breadcrumbs.get_text().lower().replace(' ', '').replace('\n', '').split("»")
    pprint(breadcrumbs)

    get_info()
    data['sourceMedia'] = 'present'  # ДОДЕЛАТЬ
    data['sourceUrl'] = url
    data['addDate'] = get_date()
    data['address'] = get_address()
    data['offerTypeCode'] = get_offer_type_code()
    data['categoryCode'] = get_category_code()
    data['buildingType'] = get_building_type()
    data['buildingClass'] = get_building_class(data['categoryCode'])
    data['typeCode'] = get_type_code()
    data['phones_import'] = get_phones()
    pprint(data)

    # return data


def get_info():
    global info
    info = {}
    all_info = soup.find_all('div', class_='notice-card__field word-break')

    for unit in all_info:
        key = unit.strong.string.lower().replace(':', '')
        value = unit.span.get_text().replace('\r', ' ').replace('\n', ' ')
        info[key] = value

    # pprint(info)


def get_date():
    tag_date = soup.find('div', class_='items-bar__group items-bar__group--double-indent')
    info_date = tag_date.get_text().lower().replace('\n', '').replace('размещено:', '').replace(' ', '')
    # pprint(info_date)

    return info_date  # ДОДЕЛАТЬ !!!


def get_address():
    if 'улица/переулок' in info:
        address = info['улица/переулок']
    elif 'местоположение' in info:
        address = info['местоположение']

    return address


def get_offer_type_code():
    type = breadcrumbs[2]

    offerTypeCode = {
        'продам': 'sale',
        'сдам': 'rent'
    }

    return offerTypeCode[type]


def get_category_code():
    category = breadcrumbs[3]

    categoryCode = {
        'жилая': 'REZIDENTIAL',
        'коммерческая': 'COMMERSIAL',
        'участкиидачи': 'LAND'
    }

    return categoryCode[category]


def get_building_type():
    return None


def get_building_class(category):
    building_class = {
        'REZIDENTIAL': None,
        'COMMERSIAL': 'A+',
        'LAND': None,
    }

    return None  # ДОДЕЛАТЬ !!!


def get_type_code():
    return None


def get_phones():
    phones = []
    tag_numbers = soup.find('div', class_='notice-card__contacts media').find('div', class_='media-body').find_all('a')

    for phone in tag_numbers:
        phones.append(str(phone.string))

    return phones


if __name__ == '__main__':
    # present_url = "https://present-dv.ru/present/notice/view/4119440"
    # present_url = "https://present-dv.ru/present/notice/view/4121240"
    # present_url = "https://present-dv.ru/present/notice/view/4165426"
    # present_url = "https://present-dv.ru/present/notice/view/4035072"
    present_url = "https://present-dv.ru/present/notice/view/4072129"
    main(present_url)
