# -*- coding: utf-8 -*-
import requests
import re
import json

_SOURCE_URL = 'http://www.whwater.com/gsfw/tstz/'
PLANED_WATER_CUT_REGEX = '<a href="./jhxts/.+?.htm" target="_blank">.+?</a>'
SUDDEN_WATER_CUT_REGEX = '<a href="./tfxts/.+?.htm" target="_blank">.+?</a>'
URL_CUT_REGEX = '\./.+?\.htm'
TITLE_CUT_REGEX = '>.+?<'

html = requests.get(_SOURCE_URL)
html_time = html.headers['Last-Modified']
html_content = requests.get(_SOURCE_URL).content.decode('utf-8')
results = re.findall('|'.join([PLANED_WATER_CUT_REGEX, SUDDEN_WATER_CUT_REGEX]), html_content)


def get_info(type):
    data = []
    if type =='jhxts':
        source = (jhxts.replace('<a href="./jhxts/">计划性停水</a>】 ', '') for jhxts in results if 'jhxts' in jhxts)
    elif type == 'tfxts':
        source = (tfxts.replace('<a href="./tfxts/">突发性停水</a>】', '') for tfxts in results if 'tfxts' in tfxts)
    else:
        return 'null'
    for accident in source:
        url = re.findall(URL_CUT_REGEX, accident)[0][2:]
        title = re.findall(TITLE_CUT_REGEX, accident)[0][1:-1]
        tmp_dict = {}
        tmp_dict['title'], tmp_dict['url'] = title, _SOURCE_URL + url
        data.append(tmp_dict)
    return data


def output():
    output_dict = {}
    output_dict['Last-Modified'] = html_time
    output_dict['jhxts'], output_dict['tfxts'] = get_info('jhxts'), get_info('tfxts')
    return json.dumps(output_dict, ensure_ascii=False)