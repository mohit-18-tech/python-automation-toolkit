# from bs4 import BeautifulSoup
# with open("toscrape.html","r") as f:
#     content=f.read()

# soup=BeautifulSoup(content,"html.parser")
# # print(soup.prettify())
# print(soup.title)
# print(soup.title.text)
# print(soup.find_all("a"))
import requests
from bs4 import BeautifulSoup
import csv 

url = "https://books.toscrape.com/"

# Get the webpage
response = requests.get(url)
response.encoding = "utf-8"

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Find all books
books = soup.find_all("article", class_="product_pod")

book_list = []

for book in books:
    # Get title
    title = book.h3.a["title"]

    # Get price
    price_text = book.find("p", class_="price_color").text

    # Keep only numbers and decimal point
    price = ""
    for ch in price_text:
        if ch.isdigit() or ch == ".":
            price += ch

    price = float(price)

    book_list.append((title, price))

# Sort by price
book_list.sort(key=lambda x: x[1])
with open("cheapest_books.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Price"])  # header row
    writer.writerows(book_list)          # writes all (title, price) tuples

# Print the 5 cheapest books
print("5 Cheapest Books:\n")

for title, price in book_list[:5]:
    print(f"{title} - £{price:.2f}")
