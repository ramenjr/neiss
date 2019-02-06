"""
This module contains functions for downloading and preprocessing NEISS data.
"""

import csv
import os

import wget

def download_raw_data(target_dir):
    """
    Downloads NEISS data, in tsv format, from the Consumer Product Safety Commission's
    website to the provided target directory, `target_dir`.

    The data is separated into one file per year, starting from 1999.

    :param target_dir: str, Pathlike
    :return: None
    """
    urls = ["https://www.cpsc.gov/cgibin/NEISSQuery/Data/Archived%20Data/{0}/neiss{0}.tsv".format(year)
            for year in range(1999, 2018)]

    for url in urls:
        filename = url.split("/")[-1]
        wget.download(url, out=os.path.abspath(os.path.join(target_dir, filename)))


def _get_header(file):
    with open(file) as f:
        header = next(f)
        return "".join([field.strip('"') for field in header])


def combine_raw_data(raw_dir, target):
    """
    Combines the raw NEISS tsv files into a single TSV file.

    :param raw_dir: str, Pathlike
    :param target: str, Pathlike
    :return: None
    """
    infiles = [os.path.join(raw_dir, file) for file in os.listdir(raw_dir) if file.endswith(".tsv")]
    with open(target, "xt", encoding="utf-8") as outfile:
        outfile.write(_get_header(infiles[0]))

        for file in infiles:
            with open(file) as infile:
                print("Now writing {} to target.".format(os.path.basename(file)))
                next(infile)
                for line in infile:
                    if line.count("\t") == 18:
                        outfile.write(line)
