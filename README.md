# Book Scraper

This project is a Python script that scrapes the website [books.toscrape.com](http://books.toscrape.com/) and saves the information of all the books on the site to a CSV file.

## Features

- The script uses the `requests`, `bs4`, and `tqdm` modules to fetch, parse, and display the progress of the scraping process.
- The script uses the `concurrent.futures` module to create a thread pool and speed up the scraping by parallelizing the requests.
- The script defines a `Book` class to store the attributes of each book, such as link, title, price, and rating.
- The script saves the scraped data to a file named `books.csv` in the same directory as the script, with the columns `Title`, `Price`, `Rating`, and `Link`.

## Usage

To run the script, you need to have Python 3 installed on your system, as well as the required modules. You can install the modules using `pip`:

```bash
pip install requests bs4 tqdm
```

Then, you can run the script from the command line:

```bash
python book_scraper.py
```

The script will start scraping the website and show a progress bar indicating the number of pages scraped. When the script finishes, it will create a `books.csv` file with the scraped data. You can open the file with any CSV viewer or editor.
