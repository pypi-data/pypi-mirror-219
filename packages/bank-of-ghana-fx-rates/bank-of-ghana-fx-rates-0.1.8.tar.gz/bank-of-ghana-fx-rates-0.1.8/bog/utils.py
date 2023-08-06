import argparse
import csv
import os
import time
from datetime import datetime
from typing import Optional, Dict, List

import click
import requests
from bs4 import BeautifulSoup
from loguru import logger
from pyfiglet import Figlet
from pathlib import Path

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


def mk_dir(path):
    """Create directory"""
    try:
        path = Path(path)
        if not path.exists():
            path.mkdir()
        else:
            logger.info(f" * Directory already exists = {path}")
    except OSError as err:
        raise OSError(f"{err}")


def save_csv(file_name: str, headers: list, lines: list, output_dir: str = None):
    """Save scraped data to CSV"""
    logger.info("Saving results in CSV...")

    if output_dir is None:
        output_dir = os.getcwd()
        os.makedirs(output_dir, exist_ok=True)
    elif not os.path.isdir(output_dir):
        raise ValueError(f"Invalid output directory: {output_dir} is not a directory")

    stamp = datetime.utcnow().strftime("%Y-%m-%d")
    file_path = os.path.join(output_dir, f"{file_name}_{stamp}.csv")
    logger.info(f"Saving file as: {file_path}")

    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        for line in lines:
            writer.writerow(line)
        # writer.writerows(lines)

    logger.info(f"{file_path} saved! Total records: {len(lines)}")


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


def scrape_table(url: str) -> Optional[Dict[str, List[str]]]:
    """Scrape table definition"""
    table = get_table_info(url)
    if table is None:
        return None

    draw = 1
    start = 0
    length = 10000
    lines = []

    while True:
        try:
            response = send_request(table["wdtNonce"], table["id"], draw, start, length)
            if not response["data"]:
                break
            for line in response['data']:
                lines.append(line)
            # lines.extend(response["data"])
            start += length
        except Exception as e:
            logger.error(f"Unsuccessful request: {e}. Trying again in few seconds.")
            time.sleep(5)

    try:
        lines.sort(key=lambda x: datetime.strptime(x[0], "%d %b %Y"), reverse=True)
    except Exception as e:
        logger.error(f"Failed to sort data: {e}")

    return {"name": table["name"], "data": lines, "headers": table["headers"]}


def get_table_info(url: str):
    """Get table information"""
    logger.info("Loading table id...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/85.0.4183.121 Safari/537.36"
    }
    try:
        html = requests.get(url, headers=headers, verify=False).text
        soup = BeautifulSoup(html, "lxml")
        table = soup.find("table", id="table_1")
        input_wdt = soup.find("input", id="wdtNonceFrontendEdit")
        if table is None or input_wdt is None:
            logger.info("Non-generic table URL. Please contact the developer.")
            return None

        # name = url.rstrip("/").split("/")[-1]
        name = url.split("/")[-2] if url[-1] in "/" else url.split("/")[-1]
        table_id = table.get("data-wpdatatable_id")
        headers = [header.get_text().strip() for header in table.find('thead').find('tr').find_all('th')]
        wdt_nonce = input_wdt.get("value")

        table_info = {
            "name": name,
            "id": table_id,
            "wdtNonce": wdt_nonce,
            "headers": headers,
        }

        logger.info(f"Table id is {table_id}")
        return table_info

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to load table information: {e}")
        return None


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
    """Info About CLI"""
    f = Figlet(font="standard", width=90)
    click.echo(f.renderText("eXchange Rate-Cli"))
    click.secho(
        "eXchange rate cli: a simple CLI for tracking exchange rates in Ghana",
        fg="cyan",
    )
    click.echo("Source of Data: Bank of Ghana [https://bog.gov.gh] ")
    click.echo("Author: Theophilus Siameh")
    click.echo("Email: theodondre@gmail.com")
