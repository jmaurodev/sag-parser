import os
import requests
import re
from csv import reader
from dotenv import load_dotenv
from zipfile import ZipFile
from tqdm import tqdm


def _load_env_vars(path=None):
    load_dotenv(path)
    env_vars = {
        'URL': os.getenv('URL'),
        'EXPECTED_FORMAT': os.getenv('EXPECTED_FORMAT')
    }
    return env_vars


def _download_file(url):
    response = requests.get(
        url,
        verify=False,
        stream=True
    )
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    file_name = 'pqd' + env_vars['EXPECTED_FORMAT']

    with open(file_name, 'wb') as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
        progress_bar.close()


def _unzip_file(file_name):
    with ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall()


def _parse(out_format=None):
    if out_format == 'json':
        pass
    elif out_format == 'csv':
        pass
    else:
        first = reader(open('ncuq.csv', encoding='latin-1'), delimiter=';')
        # second = reader(open('ncuq_det.csv'), delimiter=';')
        pattern = re.compile('[ ]+')
        for line in first:
            print(
                line[4],
                line[5],
                line[6],
                re.sub(pattern, ' ', line[10]),
            )


if __name__ == '__main__':
    env_vars = _load_env_vars()
    # _download_file(env_vars['URL'])
    # file_name = 'pqd' + env_vars['EXPECTED_FORMAT']
    # if env_vars['EXPECTED_FORMAT'] == '.zip':
    #     _unzip_file(file_name)
    _parse()
    print('Success!')
