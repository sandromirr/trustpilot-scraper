class Company:
    def __init__(self,company_name,average_rating):
        self.company_name = company_name
        self.average_rating = average_rating
        self.reviews = []

    def add_review(self,review):
        self.reviews.append(review)

    def add_reviews(self,reviews):
        self.reviews += reviews

    def __str__(self):
        return f"{self.company_name},{self.average_rating}"