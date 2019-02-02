"""
This module contains utility functions for downloading and preprocessing NEISS data.
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


def combine_raw_data(raw_dir, target_dir):
    """
    Combines the raw NEISS tsv files into a single TSV file.

    :param raw_dir: str, Pathlike
    :param target_dir: str, Pathlike
    :return: None
    """
    files = [os.path.abspath(os.path.join(raw_dir, file)) for file in os.listdir(raw_dir) if file.endswith(".tsv")]

    target_file = os.path.abspath(os.path.join(target_dir, "neiss.tsv"))

    with open(target_file, "xt") as target:
        # Writes header to file. The schema for each NEISS tsv file is
        # consistent fon a year to year basis.
        with open(files[0]) as header_file:
            reader = csv.DictReader(header_file, delimiter="\t")
            writer = csv.DictWriter(target, fieldnames=reader.fieldnames, delimiter="\t")
            writer.writeheader()

        # Writes contents to the tsv file.
        for file in files:
            with open(file) as part:
                print("Now writing {} to neiss.tsv.".format(file.name))
                reader = csv.DictReader(part, delimiter="\t")
                writer = csv.DictWriter(target, fieldnames=reader.fieldnames, delimiter="\t")
                reader.__next__()
                for row in reader:
                    writer.writerow(row)
