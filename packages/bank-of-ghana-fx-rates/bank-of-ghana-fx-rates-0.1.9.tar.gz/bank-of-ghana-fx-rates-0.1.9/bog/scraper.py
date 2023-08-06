import uuid
import urllib3
from .utils import save_csv, scrape_table, info, argParser

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GhanaRates:
    def __init__(self, url: str):
        if not url.startswith(("http://", "https://")):
            raise ValueError("Invalid URL: must start with 'http://' or 'https://'")
        self.url = url
        self.file_name = str(uuid.uuid4().hex)

    def download(self, output_dir: str = None):
        """download data"""
        table = scrape_table(self.url)

        if table:
            save_csv(
                self.file_name,
                table["headers"],
                table["data"],
                output_dir=output_dir
            )

    def get_info(self):
        info()


def cli():
    args = argParser()
    page_url = args.url

    if page_url:
        gfx = GhanaRates(url=page_url)
        gfx.download()


if __name__ == "__main__":
    cli()
