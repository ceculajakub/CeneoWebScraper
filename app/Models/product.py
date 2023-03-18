import json
import requests # TODO: fix pip direct import
from bs4 import BeautifulSoup
from review import Review

class Product:
    def __init__(self, id, name, reviews):
        self.id = id
        self.name = name
        self.reviews = reviews
    

    # mapping product to dictionary version
    def map_to_dict(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "reviews" : [review.map_to_dict() for review in self.reviews]
        }

    def write_json(self):
        with open(f"app/Mocks/{self.id}.json", "w", encoding="UTF-8") as result_file:
            json.dump(self.map_to_dict(), result_file, indent = 4)
            result_file.close()

    def read_json(self):
        with open(f"app/Mocks/{self.id}.json", "r", encoding="UTF-8") as result_file:
            result_product = json.load(result_file)
        result_file.close()
        self.name = result_product['name']
        reviews = result_product['reviews']
        for review in reviews:
            self.reviews.append(review)

    def extract(self):
        stream = requests.get("https://www.ceneo.pl/{}#tab=reviews").format(self.id)
        page_number = 2 # First iteration scrapes first page of reviews so our parameter starts from 2 
        while stream:
            page = BeautifulSoup(stream.text, "html.parser")
            reviews = page.select("div.js_product-review")

            for review in reviews:
                self.reviews.append(Review().extractReview(review).mapReview)
            stream = requests.get("https://www.ceneo.pl/{}/opinie-".format(self.productId)+str(page_number), allow_redirects=False)
            if stream.status_code == 200: # OK
                page_number +=1
            else:
                break