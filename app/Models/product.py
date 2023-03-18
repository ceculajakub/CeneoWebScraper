import json

class Product:
    def __init__(self, id, name, reviews):
        self.id = id
        self.name = name
        self.reviews = reviews
    

    # mapping product to dictionary version
    def map_to_dict(self):
        return {
            "id" : self.id,
            "name" : self.name
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