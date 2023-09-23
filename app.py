from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
import time

app = Flask(__name__)

# Define the path to your Chrome WebDriver executable
chrome_driver_path = '/Users/luke/Documents/Projects/first-chrome-extension/chromedriver'

# Configure Selenium options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run headless to avoid opening a browser window

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        asin = request.form['asin']
        
        revlist = []
    
        service = Service(executable_path='/Users/luke/Documents/Projects/first-chrome-extension/chromedriver')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')           # option so that the window doesn't pop up
        driver = webdriver.Chrome(service=service, options = options) # change filepath to downloaded webdriver

        # use selenium stealth here to bypass bot detection reliably
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        #time.sleep(1)
        driver.get('https://www.amazon.com/dp/' + asin)
        
        # get info about the product
        title = driver.find_element(By.ID, 'title')
        titlestr = title.text
        rating = driver.find_element(By.ID, 'acrPopover')
        ratingstr = rating.text
        cost = driver.find_element(By.CLASS_NAME, 'a-price-whole')
        coststr = cost.text
        
        #print('Title: ' + titlestr)
        #print('Rating: ' + ratingstr + " out of 5")
        #print('Cost: $' + coststr)

        # iterate through the pages of reviews and put them into a list
        pages = 4
        for i in range(1, pages + 1):
            driver.get('https://www.amazon.com/product-reviews/' + asin + '?pageNumber=' + str(i))
            #time.sleep(1)
            reviews = driver.find_elements(By.CLASS_NAME, 'review-text-content')
            for review in reviews:
                revlist.append(review.text)
        driver.quit()
        #print('# of reviews scraped: ' + str(len(revlist)))
        #return revlist
        #return f"""ASIN: {asin}<br>Product Title: {titlestr}
        #    <br>Product Rating: {ratingstr} out of 5
        #    <br>Product Cost: ${coststr}
        #    """
        return render_template('results.html', asin=asin, product_title=titlestr, rating=ratingstr, cost=coststr, reviews=revlist)


if __name__ == '__main__':
    app.run(debug=True)
