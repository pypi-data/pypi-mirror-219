![Python 3.7, 3.8, 3.9](https://img.shields.io/badge/Python-3.7%2C%203.8%2C%203.9-3776ab.svg?maxAge=2592000)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

### Bank of Ghana Exchange Rate Python Library
  A simple unofficial python package to scrape data bank of Ghana.
  Affiliated to [GhanaNews-Scraper](https://pypi.org/project/ghananews-scraper/) and 
  [GhanaShops-Scraper](https://pypi.org/project/ghanashops-scraper/)

### Overview
The unofficial Python API client library for Bank of Ghana allows individuals to pull historical and real-time exchange rates data using the Python programming language. 
Learn more by visiting [BoG](https://www.bog.gov.gh/treasury-and-the-markets/historical-interbank-fx-rates/)


### Example Google Colab Notebook
   Click Here: [![Google Colab Notebook](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1zZUIyp9zBhwL5CqHS3Ggf5vJCr_yTYw0?usp=sharing)


### Installation
```python
pip install bank-of-ghana-fx-rates
```
### Python Usage:
```python
from bog.scraper import GhanaRates

urls = [
    'https://www.bog.gov.gh/treasury-and-the-markets/historical-interbank-fx-rates/',
    'https://www.bog.gov.gh/treasury-and-the-markets/treasury-bill-rates/',
]
for page_url in urls:
    print(f"Downloading from : {page_url}")
    fx = GhanaRates(url = page_url)
    # download data
    fx.download()
    
    # get info
    fx.get_info()

```

### CLI Usage:
```shell
bog-fx --url 'https://www.bog.gov.gh/treasury-and-the-markets/historical-interbank-fx-rates/'
```

BuyMeCoffee
-----------
[![Build](https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png)](https://www.buymeacoffee.com/theodondrew)

Credits
-------
-  `Theophilus Siameh`
<div>
    <a href="https://twitter.com/tsiameh"><img src="https://img.shields.io/twitter/follow/tsiameh?color=blue&logo=twitter&style=flat" alt="tsiameh twitter"></a>
</div>