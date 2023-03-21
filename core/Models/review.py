from core.helpers import extract


class Review:

    # Approval and disapproval are my const values

    selectors = {
        "author": ["span.user-post__author-name"],
        "reference": ["span.user-post__author-recomendation > em"],
        "stars": ["span.user-post__score-count"],
        "content": ["div.user-post__text"],
        "assets": ["div[class*=\"positives\"] ~ div.review-feature__item", False],
        "drawbacks": ["div[class*=\"negatives\"] ~ div.review-feature__item", False],
        "is_purchased": ["div.review-pz"],
        "review_date": ["span.user-post__published > time:nth-child(1)", "datetime"],
        "purchase_date": ["span.user-post__published > time:nth-child(2)", "datetime"],
        "positive": ["span[id^='votes-yes']"],
        "negative": ["span[id^='votes-no']"]
    }

    def __init__(self, id = None, author = None, reference = None, stars = None, is_purchased = None, review_date = None, purchase_date = None, positive = None, negative = None, content = None, assets = [], drawbacks = [], approval="Polecam", disapproval="Nie polecam"):
        self.id = id
        self.author = author
        self.reference = reference
        self.stars = stars
        self.is_purchased = is_purchased
        self.review_date = review_date
        self.purchase_date = purchase_date
        self.positive = positive
        self.negative = negative
        self.content = content
        self.assets = assets
        self.drawbacks = drawbacks
        self.approval = approval
        self.disapproval = disapproval

    def map_to_Review(self):
        if self.reference == self.approval:
            self.reference = "Tak"
        elif self.reference == self.disapproval:
            self.reference = "Nie"
        else:
            self.reference = "-"
        self.stars = float(self.stars.split("/")[0].replace(",", "."))
        self.content = self.content.join(self.content.splitlines()).replace("\r\n", " ")
        if self.is_purchased == True:
            self.is_purchased = "Tak"
        else:
            self.is_purchased = "Nie"
        self.positive = int(self.positive)
        self.negative = int(self.negative)
        if not self.assets:
            self.assets = ''
        if not self.drawbacks:
            self.drawbacks = ''
        if not self.purchase_date:
            self.purchase_date = ''
        return self

    def extract_review(self, review):
        for x, y in self.selectors.items():
            setattr(self, x, extract(review, *y))
        self.id = review["data-entry-id"]
        return self
    
    def map_to_dict(self):
        return {"id": self.id} | {key: getattr(self, key) for key in self.selectors.keys()}

    def __str__(self) -> str:
        return f"id: {self.id}<br>" + "<br>".join(f"{key}: {str(getattr(self, key))}" for key in self.selectors.keys())

    def __repr__(self) -> str:
        return f"Review(id={self.id}, " + ", ".join(f"{key}={str(getattr(self, key))}" for key in self.selectors.keys()) + ")"