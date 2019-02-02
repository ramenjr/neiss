import csv
import os
from pathlib import Path
import wget

from dotenv import find_dotenv, load_dotenv

find_dotenv()
load_dotenv()

RAW_DATA_DIR = Path(os.environ["RAW_DATA_DIRECTORY"])
INTERIM_DATA_DIR = Path(os.environ["INTERIM_DATA_DIRECTORY"])

def download_raw_data():
    urls = ["https://www.cpsc.gov/cgibin/NEISSQuery/Data/Archived%20Data/{0}/neiss{0}.tsv".format(year)
            for year in range(1999,2018)]

    for url in urls:
        wget.download(url,out = str(RAW_DATA_DIR / url.split("/")[-1]))



def consolidate_raw_data():
    files = [file for file in RAW_DATA_DIR.iterdir() if file.suffix == ".tsv"]

    with open(INTERIM_DATA_DIR / "neiss.tsv", "xt") as target:
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
