import argparse
import csv
import os
import time
from datetime import datetime

import click
import requests
from bs4 import BeautifulSoup
from loguru import logger
from pyfiglet import Figlet

BASE_URL = "https://www.bog.gov.gh/wp-admin/admin-ajax.php?action=get_wdtable&table_id"


def mkdir(path):
    """Create directory"""
    try:
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            logger.info(f" * Directory already exists = {path}")
    except OSError as err:
        raise OSError(f"{err}")


def save_csv(file_name, headers, lines, output_dir=None):
    """save scraped data to csv"""
    logger.info("Saving results in csv...")

    if output_dir is None:
        output_dir = os.getcwd()
        mkdir(output_dir)
    if not os.path.isdir(output_dir):
        raise ValueError(
            f"Invalid output directory: {output_dir} is not a directory"
        )

    stamp = datetime.strftime(datetime.utcnow(), "%Y-%m-%d")
    file_path = os.path.join(output_dir, file_name + f"_{stamp}.csv")
    logger.info(f"Saving file as: {file_path}")

    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        for line in lines:
            writer.writerow(line)
    logger.info(f"{file_path}.csv saved! Total records: {len(lines)}")


def send_request(wdt, table_id, draw, start, length):
    """send request to scrape page"""
    logger.info("Scraping data from API...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/85.0.4183.121 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
    }
    data = {"draw": draw, "wdtNonce": wdt, "start": start, "length": length}
    response = requests.post(
        f"{BASE_URL}={table_id}", headers=headers, data=data, verify=False
    )
    return response.json()


def scrape_table(url: str):
    """scrape table definition"""
    table = get_table_info(url)
    if table is None:
        return
    draw = 1
    start = 0
    length = 10000
    lines = []
    while True:
        try:
            response = send_request(table["wdtNonce"], table["id"], draw, start, length)
            if len(response["data"]) > 0:
                for line in response["data"]:
                    lines.append(line)
                start += length
            else:
                break
        except:
            logger.error("Unsuccessful request. Trying again in few seconds.")
            time.sleep(5)
    try:
        lines.sort(key=lambda x: datetime.strptime(x[0], "%d %b %Y"), reverse=True)
    except:
        pass
    return {"name": table["name"], "data": lines, "headers": table["headers"]}


def get_table_info(url: str):
    """Get table information"""
    logger.info("Loading table id...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/85.0.4183.121 Safari/537.36"
    }
    html = requests.get(url, headers=headers, verify=False).text
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", id="table_1")
    input_wdt = soup.find("input", id="wdtNonceFrontendEdit")
    if table is None or input_wdt is None:
        logger.info("Non-generic table url. Please contact developer.")
        return None
    if url[-1] in "/":
        name = url.split("/")[-2]
    else:
        name = url.split("/")[-1]
    table_id = table["data-wpdatatable_id"]
    headers = []
    for header in table.find("thead").find("tr").find_all("th"):
        headers.append(header.get_text().strip())
    wdt_nonce = input_wdt["value"]
    table_info = {
        "name": name,
        "id": table_id,
        "wdtNonce": wdt_nonce,
        "headers": headers,
    }
    logger.info(f"Table id is {table_id}")
    return table_info


def argParser():
    """ArgParser Definition"""
    parser = argparse.ArgumentParser(description="Bank of Ghana FX Rates")
    parser.add_argument(
        "--url",
        "-u",
        required=True,
        default="https://www.bog.gov.gh/treasury-and-the-markets/historical-interbank-fx-rates/",
        type=str,
        help="URL to page to scrape",
    )

    args = parser.parse_args()
    return args


def info():
    """Info About CLI """
    f = Figlet(font="standard", width=90)
    click.echo(f.renderText("eXchange Rate-Cli"))
    click.secho(
        "eXchange rate cli: a simple CLI for tracking exchange rates in Ghana",
        fg="cyan",
    )
    click.echo("Source of Data: Bank of Ghana [https://bog.gov.gh] ")
    click.echo("Author: Theophilus Siameh")
    click.echo("Email: theodondre@gmail.com")
