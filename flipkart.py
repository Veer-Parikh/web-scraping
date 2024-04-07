import pandas as pd
import requests
from bs4 import BeautifulSoup

Product_Name = []
Prices = []
Description = []
Reviews = []

type_input = int(input("Enter your search type:\n1 - Mobiles Tv Laptops etc\n2 - clothes shoes bagpacks etc\n3 - Any Other\n"))
user_input = input("Enter your search query: ")
query = user_input.replace(" ", "%20")

# Define CSS selectors based on search type
type1 = {
    "Name": "_4rR01T",
    "Price": "_30jeq3 _1_WHN1",
    "Desc": "fMghEO",
    "Review": "_3LWZlK"
}
type2 = {
    "Name": "_2WkVRV",
    "Price": "_30jeq3",
    "Desc": "IRpwTa",
    "Review": "_3Ay6Sb"
}
type3 = {
    "Name": "s1Q9rs",
    "Price": "_30jeq3",
    "Desc": "_3Ay6Sb",
    "Review": "_3LWZlK"
}

# Choose CSS selectors based on user input
if type_input == 1:
    type_selector = type1
elif type_input == 2:
    type_selector = type2
elif type_input == 3:
    type_selector = type3

for i in range(1, 2):
    url = "https://www.flipkart.com/search?q=" + query + "&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=" + str(1)
    r = requests.get(url)
    print(url)
    soup = BeautifulSoup(r.text, "lxml")
    box = soup.find("div", class_="_1YokD2 _3Mn1Gg")
    # print(soup)
    names = box.find_all("div", class_=type_selector.get("Name"))
    # print(names)
    for i in names:
        name = i.text
        Product_Name.append(name)
    # print(Product_Name)

    prices = box.find_all("div", class_=type_selector.get("Price"))
    # print(names)
    for i in prices:
        price = i.text
        Prices.append(price)
    # print(Prices)

    description = box.find_all("a", class_=type_selector.get("Desc"))
    # print(names)
    for i in description:
        desc = i.text
        Description.append(desc)
    # print(Description)

    reviews = box.find_all("div", class_=type_selector.get("Review"))
    # print(names)
    for i in reviews:
        review = i.text
        Reviews.append(review)
    # print(Reviews)

# print(len(Product_Name), len(Prices), len(Description), len(Reviews))
# Prices += [None] * (max_length - len(Prices))
# Description += [None] * (max_length - len(Description))
# Reviews += [None] * (max_length - len(Reviews))

df = pd.DataFrame({
    "Product Name": Product_Name,
    "Prices": Prices,
    "Description": Description,
    "Reviews": Reviews
})

# print(df)
query.replace("%20", "_")
df.to_csv("C:\\Users\\user\\Desktop\\Veer\\WebScraping\\output files\\flipkart.csv")
