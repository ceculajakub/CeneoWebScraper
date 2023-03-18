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

    def __init__(self, id, author, reference, stars_count, is_confirmed_purchase, review_date, purchase_date, positive_counter, negative_counter, content, assets_list, drawbacks_list, approval="Polecam", disapproval="Nie polecam"):
        self.id = id
        self.author = author
        self.reference = reference
        self.stars_count = stars_count
        self.is_confirmed_purchase = is_confirmed_purchase
        self.review_date = review_date
        self.purchase_date = purchase_date
        self.positive_counter = positive_counter
        self.negative_counter = negative_counter
        self.content = content
        self.assets_list = assets_list
        self.drawbacks_list = drawbacks_list
        self.approval = approval
        self.disapproval = disapproval

    def map_to_Review(self):
        if self.reference == self.approval:
            self.reference = True
        elif self.reference == self.disapproval:
            self.reference = False
        self.stars_count = float(self.stars_count.split("/")[0].replace(",", "."))
        self.content = self.content.join(self.content.splitlines())
        self.is_confirmed_purchase = bool(self.is_confirmed_purchase)
        self.positive_counter = int(self.positive_counter)
        self.negative_counter = int(self.negative_counter)
        return self

    def extract_review(self, review):
        for x, y in self.selectors.items():
            setattr(self, x, extract(review, *y))
        self.id = review["data-entry-id"]
        return self
