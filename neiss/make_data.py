import os
import csv
from itertools import chain
from pathlib import Path


def consolidate_tsv(data_directory):
    raw_data_dir = Path(data_directory) / "raw"
    interim_data_dir = Path(data_directory) / "interim"

    files = [file for file in raw_data_dir.iterdir() if file.suffix == ".tsv"]

    with open(interim_data_dir / "neiss.tsv", "xt") as target:
        # Writes header to file first. The schema for each NEISS tsv file is
        # consistent fon a year to year basis.
        with open(files[0]) as header_file:
            reader = csv.DictReader(header_file,delimiter="\t")
            writer = csv.DictWriter(target, fieldnames=reader.fieldnames,delimiter="\t")
            writer.writeheader()

        # Writes contents to the tsv file.
        for file in files:
            with open(file) as part:
                print("Now writing {} to neiss.tsv.".format(file.name))
                reader = csv.DictReader(part, delimiter="\t")
                writer = csv.DictWriter(target, fieldnames=reader.fieldnames,delimiter="\t")
                reader.__next__()
                for row in reader:
                    writer.writerow(row)

