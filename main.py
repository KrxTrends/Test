from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import urllib.parse


def scrape_threads(df_trends):
    chrome_options = Options()
    chrome_options.binary_location = '/opt/render/project/.render/chrome/opt/google/chrome/usr/bin/google-chrome'
    # options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Runs without GUI
    chrome_options.add_argument("--disable-gpu")  # Prevents graphics processing
    chrome_options.add_argument("--no-sandbox")  # Improves performance on some systems
    chrome_options.add_argument("--disable-dev-shm-usage")  # Prevents crashes on limited memory
    
    service = Service('/opt/render/project/.render/chrome/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    results = []

    for index, trend_name in enumerate(df_trends['trend_name']):
        try:
            search_expression = urllib.parse.quote(trend_name)
            driver.get(f"https://www.threads.net/search?q={search_expression}")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.x1a6qonq.x6ikm8r.x10wlt62.xj0a0fe.x126k92a.x6prxxf.x7r5mf7"))
            )
        
            # Find all divs containing the text
            divs = driver.find_elements(By.CSS_SELECTOR, "div.x1a6qonq.x6ikm8r.x10wlt62.xj0a0fe.x126k92a.x6prxxf.x7r5mf7")
            times = driver.find_elements(By.CSS_SELECTOR, "time.x1rg5ohu.xnei2rj.x2b8uid.xuxw1ft")
            
            # Extract text and store each as a separate record
            for div, time_element in zip(divs, times):
                text = " ".join([span.text for span in div.find_elements(By.TAG_NAME, "span") if span.text.strip()])
                timestamp = time_element.get_attribute('title')  # Get the time 'title' attribute
                results.append({"fk_summarised_trend_id": df_trends.fk_summarised_trend_id[index], "Text": text, "Timestamp": timestamp})
                
        except Exception as e:
            return f"Failed scraping threads.net for {trend_name} due to error {e}"
    driver.quit()

    results = pd.DataFrame(results).drop_duplicates().reset_index(drop=True)
    return pd.DataFrame(results)



def main():
    hot_trends = pd.DataFrame({
        'fk_summarised_trend_id': [123,456,789],
        'trend_name': ['Bruno Fernandes','Massive','Columbia University']
    })
    
    df_threads = scrape_threads(hot_trends)
    print(df_threads.head(3))

if __name__ == "__main__":
    main()

