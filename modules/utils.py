import os
import typing as T
import math
import concurrent.futures
import time
import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

def build_path(dir: str = ""):
    path = str(os.path.dirname((os.path.realpath(__file__))))
    path = path + "/" + dir
    return path.replace("\\", "/")


def get_root_directory(root_name='scraping-houzz_de'):
    sep_path = build_path().split("/")
    root_sep_path = sep_path[: sep_path.index(root_name) + 1]
    return "/".join(root_sep_path)


def coalesce(source: T.Dict[str, str], target: T.Dict[str, str]):
    for key in target:
        value = target[key] if (target[key] or key not in source) else source[key]
        target[key] = value
    return target


def split_chunks(
    iterables: T.Iterable[T.Any], size=12
) -> T.Tuple[T.Iterable]:
    num_of_chunks = math.ceil(len(iterables) / size)
    return tuple(
        iterables[idx * size : (idx + 1) * size] for idx in range(num_of_chunks)
    )


def clean_text(remove_chars: T.List[str], text: str):
    new_text = text
    for remove_char in remove_chars:
        new_text = re.sub(remove_char, "", new_text)
    return new_text


def parallelize(
    iterables: T.Iterable,
    function: T.Callable,
    timeout: int = None,
    idle_time: float = 4,
    concurrency: int = 12,
):
    print("Parallelism factor:", concurrency)
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        step = concurrency
        idx = 0
        output = []
        while True:
            iterables_range = (idx * step, (idx + 1) * step)
            iterable = iterables[iterables_range[0]: iterables_range[1]]
            if len(iterable):
                try:
                    for res in executor.map(function, iterable, timeout=timeout):
                        output.append(res)
                except Exception as error:
                    print('Error:', str(error))
                    print('Error segment:', iterables_range, iterable)
                    exit()

                idx += 1
                print('Processed', len(output), 'inputs.', 'Idle for', idle_time, 'sec')
                time.sleep(idle_time)
            else:
                break
        return output

def get_content(wait_time: float, base_url: str = None):
    def fetch(url: str):
        opts = webdriver.ChromeOptions()
        opts.add_argument("--headless")
        opts.add_argument("--log-level=OFF")
        driver = webdriver.Chrome(options=opts)
        driver.get(url)
        WebDriverWait(driver, wait_time)
        content = driver.page_source
        driver.close()
        return content

    url = base_url
    if url is None:
        return None
    print(url)
    return fetch(url)

def scrape(url: str, output_path: str, wait_time: float):
    with open(output_path, 'w', encoding='utf-8') as file:
        content = get_content(wait_time, url)
        file.write(content)
        return content

def get_or_scrape_content(url: str, output_path: str, wait_time = 10):
    if os.path.isfile(output_path):
        with open(output_path, 'r', encoding='utf-8') as file:
            content = file.read()
        if not content:
            content = scrape(url, output_path, wait_time)
    else:
        content = scrape(url, output_path, wait_time)
    return content
