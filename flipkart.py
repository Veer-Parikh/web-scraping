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

if type_input == 1:
    for i in range(1,10):
        url = "https://www.flipkart.com/search?q=" + query + "&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=" + str(i)
        r = requests.get(url)
        print(r)
        print(url)
        soup = BeautifulSoup(r.text, "lxml")
        box = soup.find("div", class_="_1YokD2 _3Mn1Gg")
        # print(soup)

        names = box.find_all("div", class_="_4rR01T")
        for i in names:
            name = i.text
            Product_Name.append(name)
        # print(Product_Name)

        prices = box.find_all("div", class_="_30jeq3 _1_WHN1")
        for i in prices:
            price = i.text
            Prices.append(price)
        # print(Prices)

        description = box.find_all("div", class_="fMghEO")
        for i in description:
            desc = i.text
            Description.append(desc)
        # print(Description)

        reviews = box.find_all("div", class_="_3LWZlK")
        for i in reviews:
            review = i.text
            Reviews.append(review)
        # print(Reviews)
        
        # max_length = max(len(Product_Name), len(Prices), len(Description), len(Reviews))
        # if max_length > 0:
        #     Prices += [None] * (max_length - len(Prices))
        #     Description += [None] * (max_length - len(Description))
        #     Reviews += [None] * (max_length - len(Reviews))

        # print(len(Product_Name))
        # print(len(Prices))
        # print(len(Reviews))
        # print(len(Description))
        df = pd.DataFrame({
            "Product Name": Product_Name,
            "Prices": Prices,
            "Description": Description,
            "Reviews": Reviews
        })
        new = query.replace("%20", "_")
        df.to_csv("C:\\Users\\user\\Desktop\\Veer\\WebScraping\\output files\\"+new+"_flipkart.csv")

elif type_input == 2:
    for i in range(1,10):
        url = "https://www.flipkart.com/search?q=" + query + "&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=" + str(i)
        r = requests.get(url)
        print(url)
        soup = BeautifulSoup(r.text, "lxml")
        box = soup.find("div", class_="_1YokD2 _3Mn1Gg")
        # print(soup)

        names = box.find_all("div", class_="_2WkVRV")
        for i in names:
            name = i.text
            Product_Name.append(name)
        # print(Product_Name)

        prices = box.find_all("div", class_="_30jeq3")
        for i in prices:
            price = i.text
            Prices.append(price)
        # print(Prices)

        description = box.find_all("a", class_="IRpwTa")
        if not description:
           description = box.find_all("a", class_="IRpwTa _2-ICcC")
        for i in description:
            desc = i.text
            Description.append(desc)
        # print(Description)

        
        # print(len(Product_Name))
        # print(len(Prices))
        # print(len(Reviews))
        # print(len(Description))

        # reviews = box.find_all("div", class_="_3LWZlK")
        # for i in reviews:
        #     review = i.text
        #     Reviews.append(review)
        # print(Reviews)

        df = pd.DataFrame({
            "Product Name": Product_Name,
            "Prices": Prices,
            "Description": Description
        })
        new = query.replace("%20", "_")
        df.to_csv("C:\\Users\\user\\Desktop\\Veer\\WebScraping\\output files\\"+new+"_flipkart.csv")


elif type_input == 3:
    for i in range(1,5):
        
        url = "https://www.flipkart.com/search?q=" + query + "&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=" + str(i)
        r = requests.get(url)
        print(url)
        soup = BeautifulSoup(r.text, "lxml")
        box = soup.find("div", class_="_1YokD2 _3Mn1Gg")
        # print(soup)

        names = box.find_all("a", class_="s1Q9rs")
        for i in names:
            name = i.text
            Product_Name.append(name)
        # print(Product_Name)

        prices = box.find_all("div", class_="_30jeq3")
        if not prices:
            prices = box.find_all("div", class_="_2Tpdn3")
        for i in prices:
            price = i.text
            Prices.append(price)
        # print(Prices)

        # description = box.find_all("a", class_="fMghEO")
        # for i in description:
        #     desc = i.text
        #     Description.append(desc)
        # print(Description)
        
        reviews = box.find_all("div", class_="_3LWZlK")
        if not reviews:
            reviews = box.find_all("div", class_="_3Djpdu")
        for i in reviews:
            review = i.text
            Reviews.append(review)
        # print(Reviews)
        max_length = max(len(Product_Name), len(Prices), len(Description), len(Reviews))
        Prices += [None] * (max_length - len(Prices))
        Description += [None] * (max_length - len(Description))
        Reviews += [None] * (max_length - len(Reviews))

        
        print(len(Product_Name))
        print(len(Prices))
        print(len(Reviews))
        df = pd.DataFrame({
            "Product Name": Product_Name,
            "Prices": Prices,
            # "Description": Description,
            "Reviews": Reviews
        })
        new  = query.replace("%20", "_")
        df.to_csv("C:\\Users\\user\\Desktop\\Veer\\WebScraping\\output files\\"+new+"_flipkart.csv")

    

# print(len(Product_Name), len(Prices), len(Description), len(Reviews))
# Prices += [None] * (max_length - len(Prices))
# Description += [None] * (max_length - len(Description))
# Reviews += [None] * (max_length - len(Reviews))

