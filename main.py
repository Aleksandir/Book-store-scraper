import requests
from bs4 import BeautifulSoup


class Book:
    def __init__(self, link, title, price, rating):
        self.link = link
        self.title = title
        self.price = price
        self.rating = rating

    def __str__(self):
        return f"{self.title} - {self.price} - {self.rating}"


def main():
    URL = "http://books.toscrape.com"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    soup = soup.find_all(class_="product_pod")

    books = []
    for book in soup:
        # <a href="catalogue/the-boys-in-the-boat-nine-americans-and-their-epic-quest-for-gold-at-the-1936-berlin-olympics_992/index.html"><img src="media/cache/66/88////66883b91f6804b2323c8369331cb7dd1.jpg" alt="The Boys in the Boat: Nine Americans and Their Epic Quest for Gold at the 1936 Berlin Olympics" class="thumbnail"></a>
        link = book.find("a").get("href")

        # <img src="media/cache/66/88/66883b91f6804b2323c8369331cb7dd1.jpg" alt="The Boys in the Boat: Nine Americans and Their Epic Quest for Gold at the 1936 Berlin Olympics" class="thumbnail">
        title = book.find("h3").find("a")["title"]
        title = title.replace(",", "")

        # <div class="product_price">
        # <p class="price_color">£22.60</p>
        price = book.find(class_="price_color").get_text()

        # <p class="star-rating Three">
        rating = book.find(class_="star-rating")["class"][1]
        books.append(Book(link, title, price, rating))

    with open("books.csv", "w") as file:
        file.write("Title,Price,Rating,Link\n")
        for book in books:
            file.write(f"{book.title},{book.price},{book.rating},{URL}/{book.link}\n")


if __name__ == "__main__":
    main()
