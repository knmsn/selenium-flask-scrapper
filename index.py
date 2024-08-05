from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400

    chromedriver_autoinstaller.install()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(f"https://www.google.com/search?q={query}")
    results = driver.find_elements(By.CSS_SELECTOR, 'div.g')

    output = []
    for result in results:
        try:
            title = result.find_element(By.TAG_NAME, 'h3').text
            link = result.find_element(By.TAG_NAME, 'a').get_attribute('href')
            output.append({'title': title, 'link': link})
        except:
            continue

    driver.quit()
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)
