import pandas as pd
import requests
from bs4 import BeautifulSoup

Product_Name = []
Prices = []
Description = []
Reviews = []

# type_input = int(input("Enter your search type:\n1 - Mobiles Tv Laptops etc\n2 - clothes shoes bagpacks etc\n3 - Any Other\n"))
# user_input = input("Enter your search query: ")
# query = user_input.replace(" ", "%20")

url = "https://www.google.com/search?sca_esv=383fc29145713f41&rlz=1C1CHBF_enIN1039IN1039&q=shoes+for+men&tbm=shop&source=lnms&prmd=sivnmbtz&ved=1t:200715&ictx=111&biw=1920&bih=953&dpr=1"
r = requests.get(url)
print(r)
print(url)
soup = BeautifulSoup(r.text, "lxml")
# box = soup.find("div", class_="sh-sr__shop-result-group Qlx7of")
# print(box)

names = soup.find("div", class_="EI11Pd")
print(names)
# newnames = names.find("h3", class_="tAxDx")

# for i in newnames:
#     name = i.text
#     Product_Name.append(name)
    
# print(Product_Name)