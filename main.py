from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class Book:
    def __init__(self, link, title, price, rating):
        self.link = link
        self.title = title
        self.price = price
        self.rating = rating

    def __str__(self):
        return f"{self.title} - {self.price} - {self.rating} - {self.link}"


def main():
    # clear the file or create it if it doesn't exist
    with open("books.csv", "w") as file:
        file.write("Title,Price,Rating,Link\n")

    max_page = get_max_page("http://books.toscrape.com/catalogue/page-1.html")

    # Create a thread pool with 10 threads and map the scrape_page function to each page
    # tqdm is used to display a progress bar, and list() is used to force the executor to start executing
    with ThreadPoolExecutor(max_workers=10) as executor:
        list(tqdm(executor.map(scrape_page, range(1, max_page + 1)), total=max_page))


def scrape_page(i):
    """
    Scrapes a webpage and saves the books found on that page.

    Args:
        i (int): The page number to scrape.

    Returns:
        None
    """
    URL = f"http://books.toscrape.com/catalogue/page-{i}.html"
    books = get_books(URL)
    save_books(books)


def save_books(books, URL="http://books.toscrape.com/catalogue"):
    with open("books.csv", "a") as file:
        for book in books:
            file.write(f"{book.title},{book.price},{book.rating},{URL}/{book.link}\n")


def get_max_page(URL):
    """
    Retrieves the maximum page number from a given URL.

    Args:
        URL (str): The URL to scrape.

    Returns:
        int: The maximum page number found on the webpage.
    """
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    soup = soup.find(class_="pager").find("li").get_text()
    # Split the text by spaces
    parts = soup.split()

    # The last part should be the maximum page number
    max_page = parts[-1]

    # Convert the maximum page number to an integer and return it
    return int(max_page)


def get_books(URL):
    """
    Retrieves a list of books from the given URL.

    Parameters:
    URL (str): The URL of the webpage containing the books.

    Returns:
    list: A list of Book objects, each representing a book with its link, title, price, and rating.
    """
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    soup = soup.find_all(class_="product_pod")

    books = []
    for book in soup:
        # get link
        link = book.find("a").get("href")

        # get title
        title = book.find("h3").find("a")["title"]
        title = title.replace(",", "")

        # get price
        price = book.find(class_="price_color").get_text()

        # <p class="star-rating Three">
        rating = book.find(class_="star-rating")["class"][1]
        books.append(Book(link, title, price, rating))

    return books


if __name__ == "__main__":
    main()
