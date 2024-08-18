from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import sys
import time

# Read command-line arguments
if len(sys.argv) < 3:
    print('Usage: python dom.py <url> <params-file>')
    sys.exit(1)

url_template = sys.argv[1]
params_file = sys.argv[2]

# Extract the value from the URL (e.g., "cyrex")
value_to_check = url_template.split('=')[1]

# Read parameters from file
with open(params_file, 'r') as f:
    parameters = [line.strip() for line in f if line.strip()]

# Set up Selenium WebDriver with optimized options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run headlessly (without GUI)
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-images')  # Disable loading images to save resources
chrome_options.add_argument('--blink-settings=imagesEnabled=false')
chrome_options.page_load_strategy = 'eager'  # Make the driver return control sooner
service = Service('/home/kali/Desktop/New-Folder/PRO-PLAN/xss-checker-linux/chromedriver')  # Update path to your chromedriver

# Function to test all parameters in a single WebDriver session
def test_parameters():
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(13)  # Set a page load timeout
    driver.set_script_timeout(13)     # Set a script timeout
    
    try:
        for param in parameters:
            test_url = url_template.replace('FUZZ', param)
            try:
                driver.get(test_url)

                # Check if the specific value (e.g., "cyrex") is reflected in the DOM
                page_source = driver.page_source
                is_reflected = value_to_check in page_source

                if is_reflected:
                    print(f'Value "{value_to_check}" is reflected in the DOM on URL: {test_url}')
            except Exception as e:
                print(f"Error processing {test_url}: {e}")
    finally:
        driver.quit()

# Run the test
start_time = time.time()
test_parameters()
end_time = time.time()
print(f"Completed in {end_time - start_time:.2f} seconds")
