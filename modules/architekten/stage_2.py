import os
import bs4
import json
import modules.utils as utils
import modules.architekten.const as const

NAME = const.NAME
ROOT_DIR = utils.get_root_directory()
HTML_DIR = f'{ROOT_DIR}/out/html/{NAME}/stage-2'
JSON_DIR = f'{ROOT_DIR}/out/json/{NAME}/stage-2'

os.makedirs(HTML_DIR, exist_ok=True)

def get_info(content: str, url: str):    
    parsed_page = bs4.BeautifulSoup(content, 'html.parser')
    title = parsed_page.find([f'h{n}' for n in range(1, 7)], {'data-component': 'Pro Name'}).string
    _format = {
        "business_name": "p",
        "phone_number": "p",
        "website": "div",
        "address": "span",
    }
    output = {
        key: None
        for key in _format
    }
    translate = {
        "Unternehmensname": "business_name",
        "Telefonnummer": "phone_number",
        "Website": "website",
        "Adresse": "address"
    }

    business_details = parsed_page.find('div', {'data-container': 'Business Details'}).find_all('div', recursive=False)
    
    for business_detail in business_details:
        key = business_detail.find('h3').string.strip()
        key = translate[key] if key in translate else None
        if key is None:
            continue
        details = business_detail.find_all(_format[key])
        detail_list = []
        for detail in details:
            detail_list.append(detail.string if detail.string else detail.get_text())
        detail_string = ' '.join(detail_list).replace('\n', '')
        output[key] = ' '.join(detail_string.split())
        
    if not output['business_name']:
        print(f'Coalesced business name for `{url}`')
        output['business_name'] = title
    
    output['url'] = url
    
    return output

def scrape(url: str):
    filename = url.split('/')[-1].split('~')[0]
    output_path = HTML_DIR + '/' + filename + '.html'
    content = utils.get_or_scrape_content(url, output_path, 5)
    info = get_info(content, url)
    return info

def run():
    urls = []
    with open(JSON_DIR[: JSON_DIR.index('stage-2')] + 'stage-1/urls.json', 'r', encoding='utf-8') as file:
        urls = json.load(file)
    info = utils.parallelize(urls, scrape, idle_time=0.5)
    os.makedirs(JSON_DIR, exist_ok=True)
    with open(JSON_DIR + '/info.json', 'w', encoding='utf-8') as file:
        json.dump(info, file, indent=4)