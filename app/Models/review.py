class Review:

    def __init__(self, id, author, reference, stars_count, is_confirmed_purchase, review_date, purchase_date, positive_counter, negative_counter, content, assets_list, drawbacks_list):
        self.id = id
        self.author = author
        self.reference = reference
        self.stars_count = stars_count
        self.is_confirmed_purchase = is_confirmed_purchase
        self.review_date = review_date
        self.purchase_date = purchase_date
        self.positive_counter =positive_counter
        self.negative_counter = negative_counter
        self.content = content
        self.assets_list = assets_list
        self.drawbacks_list = drawbacks_list
    