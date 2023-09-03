import utils
import os
import bs4
import json
import const

URL = const.URL
NAME = const.NAME
ROOT_DIR = utils.get_root_directory()
HTML_DIR = f'{ROOT_DIR}/out/html/{NAME}/stage-1'
JSON_DIR = f'{ROOT_DIR}/out/json/{NAME}/stage-1'

os.makedirs(HTML_DIR, exist_ok=True)

def get_page_url(content: str):
    parsed_page = bs4.BeautifulSoup(content, 'html.parser')
    elements = parsed_page.find_all('a', {'class': 'hz-pro-ctl'})
    hrefs = [element['href'] for element in elements if element.get('href', None) is not None]
    return hrefs

output_urls = []

for idx in range(0, 40):
    url = URL
    number = idx * 15
    if number != 0:
        url += f'/p/{number}'
    output_path = HTML_DIR
    filename = f'index-{idx}.html'
    print(f'getting {filename} ...')
    content = utils.get_or_scrape_content(url, output_path + '/' + filename)
    urls = get_page_url(content)
    if len(urls):
        output_urls.extend(urls)
    else:
        break

os.makedirs(JSON_DIR, exist_ok=True)
with open(JSON_DIR + '/urls.json', 'w') as file:
    json.dump(output_urls, file, indent=4)
    
print(f'got {len(output_urls)} urls')