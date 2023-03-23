import json
import requests
from bs4 import BeautifulSoup
from core.Models.review import Review
from core.helpers import extract


class Product:
    def __init__(self, id, name="",  reviews_counted=0, drawbacks_counted=0, assets_counted=0, average_stars=0.0, reviews=[]):
        self.id = id
        self.name = name
        self.reviews_counted = reviews_counted
        self.drawbacks_counted = drawbacks_counted
        self.assets_counted = assets_counted
        self.average_stars = average_stars
        self.reviews = reviews.copy()

    # mapping product to dictionary version

    def map_to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "reviews": [review.map_to_dict() for review in self.reviews]
        }

    def write_json(self):
        with open(f"core/Mocks/{self.id}.json", "w", encoding="UTF-8") as result_file:
            json.dump(self.map_to_dict(), result_file,
                      indent=4, ensure_ascii=False)
            result_file.close()

    def read_json(self):
        with open(f"core/Mocks/{self.id}.json", "r", encoding="UTF-8") as result_file:
            result_product = json.load(result_file)
        result_file.close()
        self.name = result_product['name']
        reviews = result_product['reviews']
        for review in reviews:
            self.reviews.append(review)

    def extract(self):
        stream = requests.get(
            "https://www.ceneo.pl/{}#tab=reviews".format(self.id), headers={'Connection': 'close'})
        # First iteration scrapes first page of reviews so our parameter starts from 2
        page_number = 2
        while stream:
            page = BeautifulSoup(stream.text, "html.parser")
            reviews = page.select("div.js_product-review")

            for review in reviews:
                self.reviews.append(
                    Review().extract_review(review).map_to_Review())
            stream = requests.get("https://www.ceneo.pl/{}/opinie-".format(self.id)+str(
                page_number), allow_redirects=False, headers={'Connection': 'close'})
            if stream.status_code == 200:  # OK
                page_number += 1
            else:
                break

    def get_name(self):
        with requests.Session() as session:
            stream = session.get(
                "https://www.ceneo.pl/{}#tab=reviews".format(self.id), headers={'Connection': 'close'})
            if stream.status_code == 200:  # OK
                page = BeautifulSoup(stream.text, 'html.parser')
                self.name = extract(page, '.js_product-h1-link')

    def __str__(self) -> str:
        return f"id: {self.id}<br>name: {self.name}<br>reviews<br><br>" + "<br><br>".join(str(review) for review in self.reviews)

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name={self.name}, reviews=[" + ", ".join(review.__repr__() for review in self.reviews) + "])"

    def stats_counter(self):
        self.reviews_counted = len(self.reviews)
        for review in self.reviews:
            if review['drawbacks'] != None:
                self.drawbacks_counted += len(review['drawbacks'])
            if review['assets'] != None:
                self.assets_counted += len(review['assets'])
            self.average_stars += review['stars']
        self.average_stars /= self.reviews_counted
