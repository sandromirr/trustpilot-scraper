import requests
from bs4 import BeautifulSoup

from Company import Company
from Review import Review,ReviewScrape,ReviewUtil

if __name__ == "__main__":
    url = 'https://www.trustpilot.com/review/fountainheadme.com'
    page = requests.get(url).text

    soap = BeautifulSoup(page,'html.parser')

    name = soap.find('span',{'class':'multi-size-header__big'}).text.strip()
    average_rating = soap.find('p',{'class':'header_trustscore'}).text.strip()
    review_count = int(soap.find('h2',{'class':'header--inline'}).text.strip().split('•')[0].replace(',',''))

    pages = review_count // 20

    if review_count % 20 != 0:
        pages = review_count // 20 + 1

    #print(review_count,pages)
    company = Company(name,average_rating)
    review_scrapper = ReviewScrape()
    pages = 2
    for page in range(1,pages+1):
        page_url = f'{url}?languages=all&page={page}'
        company.add_reviews(review_scrapper.scrape(page_url))

    ReviewUtil.save(f'{company.company_name}.csv',company.reviews)
    #print(ReviewUtil.validate('122@ dsf@'))



