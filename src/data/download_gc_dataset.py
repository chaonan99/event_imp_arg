import argparse
from os.path import basename, exists, join
from zipfile import ZipFile

import requests

from config import cfg
from utils import log
from data import gc_dataset_name, gc_dataset_url


def download_gc_dataset(url, path):
    # download dataset from url
    log.info('Downloading dataset from {} to {}'.format(url, path))

    dataset_name = basename(url)
    file_path = join(path, dataset_name)

    response = requests.get(url)
    with open(file_path, 'wb') as fout:
        fout.write(response.content)

    # unzip dataset
    log.info('Extracting zipped dataset from {}'.format(file_path))
    dataset_zip = ZipFile(file_path)
    dataset_zip.extractall(path)
    dataset_zip.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='url of the dataset',
                        default=gc_dataset_url)
    parser.add_argument('--path', help='directory to store the downloaded file',
                        default=cfg.raw_data_path)
    args = parser.parse_args()

    if not exists(join(args.path, gc_dataset_name)):
        download_gc_dataset(url=args.url, path=args.path)
    else:
        log.info('Dataset already exists: {}'.format(
            join(args.path, gc_dataset_name)))
