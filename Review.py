from bs4 import BeautifulSoup
import requests
import csv

class Review:
    def __init__(self,name,photo,location,rate,title,text):
        self.name = name
        self.photo = photo
        self.location = location
        self.rate = rate
        self.text = text
        self.title = title

    def __str__(self):
        return f"{self.name} {self.photo} {self.location} {self.rate} {self.text} {self.title}"


class ReviewScrape:
    def scrape(self,url):
        page = requests.get(url).text
        soap = BeautifulSoup(page, 'html.parser')
        reviews = soap.find_all('div', {'class': 'review-card'})
        page_reviews = []
        for review in reviews:
            customer_name = review.find('div', {'class': 'consumer-information__name'}).text.strip()
            photo = 'NO photo'
            if review.find('consumer-review-picture').has_attr('consumer-image-url'):
                    photo = review.find('consumer-review-picture')['consumer-image-url']
            location = 'No Location'
            if review.find('div', {'class': 'consumer-information__location'}):
                location = review.find('div', {'class': 'consumer-information__location'}).span.text.strip()
            customer_rate = review.find('div', {'class': 'star-rating star-rating--medium'}).img['alt'].strip()
            customer_title = 'NO COMMENT TITLE'
            if review.find('a', {'class': 'link link--large link--dark'}):
                customer_title = review.find('a', {'class': 'link link--large link--dark'}).text.strip()
            customer_text = 'NO COMMENT BODY'
            if review.find('p', {'class': 'review-content__text'}):
                customer_text = review.find('p', {'class': 'review-content__text'}).text.strip()
            customer_review = Review(customer_name, photo, location, customer_rate, customer_title, customer_text)
            page_reviews.append(customer_review)
        return page_reviews

def validate(str):
    x = '\/:.0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz '
    s = ''
    for i in str:
        if i in x:
            s += i
    return s


class ReviewUtil:
    @staticmethod
    def save(file_name,reviews):
        fields = ['name','photo','location','rate','title','text']
        rows = []
        for review in reviews:
            rows.append([
                validate(review.name),
                validate(review.photo),
                validate(review.location),
                validate(review.rate),
                validate(review.title),
                validate(review.text)
            ])
        with open(file_name, 'w',newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            csvwriter.writerows(rows)