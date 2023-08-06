from setuptools import find_packages, setup

with open("README.md") as f:
    README = f.read()

with open("requirements.txt", "r") as f:
    install_requires = f.read().splitlines()

setup(
    name='bank-of-ghana-fx-rates',
    py_modules=["bog"],
    version='0.1.8',
    packages=find_packages(exclude=["docs", "tests", "tests.*"]),
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/donwany/bank-of-ghana-fx-rates.git',
    license="MIT License",
    author="Theophilus Siameh",
    author_email="theodondre@gmail.com",
    install_requires=install_requires,
    description='A python client library used to extract the exchange rates of Bank of Ghana into CSV',
    entry_points={
        "console_scripts": [
            "bog-fx = bog.scraper:cli",
        ]
    },
    classifiers=[
        # See https://pypi.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
    ],
    keywords='Bank of Ghana, Ghana, Ghana API, Bank of Ghana Exchange Rates, government of Ghana, finance, APIs',
    platforms=["any"],
    python_requires=">=3.5",
)
