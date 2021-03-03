import requests
from bs4 import BeautifulSoup

from Company import Company
from Review import ReviewScrape,ReviewUtil

if __name__ == "__main__":
    url = 'https://www.trustpilot.com/review/github.com'
    page = requests.get(url).text

    soap = BeautifulSoup(page,'html.parser')

    name = soap.find('span',{'class':'multi-size-header__big'}).text.strip()
    average_rating = soap.find('p',{'class':'header_trustscore'}).text.strip()
    review_count = int(soap.find('h2',{'class':'header--inline'}).text.strip().split('•')[0].replace(',',''))

    review_per_page = 20
    pages = review_count // review_per_page

    if review_count % review_per_page != 0:
        pages = review_count // review_per_page + 1

    company = Company(name,average_rating)
    review_scrapper = ReviewScrape()
    for page in range(1,pages+1):
        page_url = f'{url}?languages=all&page={page}'
        company.add_reviews(review_scrapper.scrape(page_url))

    ReviewUtil.save(f'{company.company_name}.csv',company.reviews)



