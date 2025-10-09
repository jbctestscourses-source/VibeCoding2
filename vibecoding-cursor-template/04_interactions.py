# 04 - Interactions

# 01 Create a program that jiggles the mouse so that the computer doesn't go to sleep
""" 
    Make a program that:
        1. Jiggles the mouse so that the computer doesn't go to sleep
"""
import pyautogui
import time

print("Mouse Jiggler Started!")
print("This will gently move your mouse every 30 seconds to keep your computer awake.")
print("Press Ctrl+C to stop the program.")

try:
    while True:
        # Get the current mouse position
        current_x, current_y = pyautogui.position()
        
        # Move mouse slightly to the right
        pyautogui.moveRel(10, 0, duration=0.1)
        time.sleep(0.1)
        
        # Move mouse back to original position
        pyautogui.moveRel(-10, 0, duration=0.1)
        
        print("Mouse moved - computer kept awake!")
        
        # Wait 30 seconds before next movement
        time.sleep(30)
        
except KeyboardInterrupt:
    print("\nMouse Jiggler stopped. Your computer can now sleep normally.")

# 02 Create a python program that asks the user for a URL and downloads the corresponding video in the lowest quality. Use a reliable library and no APIs.
""" 
    Make a program that:
        1. Asks the user for a URL
        2. Downloads the corresponding video in the lowest quality
"""
import yt_dlp
import os
import ssl
import certifi

# Fix SSL certificate issues on macOS
ssl._create_default_https_context = ssl._create_unverified_context
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

def download_video():
    print("Video Downloader")
    print("This program downloads videos from URLs in the lowest quality.")
    print("Supported sites: YouTube, Vimeo, and many others!")
    
    # Ask user for URL
    url = input("Please enter the video URL: ").strip()
    
    if not url:
        print("No URL provided. Exiting...")
        return
    
    # Configure yt-dlp to download in lowest quality
    ydl_opts = {
        'format': 'worst',  # Downloads the worst/lowest quality available
        'outtmpl': '%(title)s.%(ext)s',  # Save with video title as filename
        'no_check_certificate': True,  # Skip SSL certificate verification to fix macOS issues
        'extractor_retries': 3,  # Retry failed downloads
        'socket_timeout': 30,  # Set timeout to avoid hanging
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Starting download...")
            ydl.download([url])
            print("Download completed successfully!")
            
    except Exception as e:
        print(f"Error downloading video: {e}")
        print("Please check the URL and try again.")

# Run the downloader
if __name__ == "__main__":
    download_video()


# 03 Automate your browser to answer this survey: https://forms.gle/uXPeoEpXkdFEfRw49
""" 
    Make a program that:
        1. Opens the browser
        2. Navigates to the survey URL
        3. Answers the survey
"""
# Survey Automation Program
# This program automatically fills out a Google form

#pip install selenium webdriver-manager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def fill_survey():
    print("Survey Automation Program")
    print("This program will automatically fill out the Google form for you.")
    print("Make sure you have Chrome browser installed!")
    
    # Get user information
    print("\nPlease provide the information for the survey:")
    name = input("Enter your name: ").strip()
    email = input("Enter your email: ").strip()
    address = input("Enter your address: ").strip()
    phone = input("Enter your phone number: ").strip()
    comments = input("Enter any comments (optional): ").strip()
    
    if not name or not email or not address or not phone:
        print("Please provide all required information (name, email, address, phone).")
        return
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        # Start the browser
        print("\nOpening browser...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://forms.gle/uXPeoEpXkdFEfRw49")
        
        # Wait for the page to load
        wait = WebDriverWait(driver, 10)
        
        print("Filling out the form...")
        
        # Wait a bit for the form to fully load
        time.sleep(3)
        
        # Find all input fields in order (including comments which is also an input)
        all_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='email']")
        print(f"Found {len(all_inputs)} input fields")
        
        # Let's debug by showing what we find
        for i, input_field in enumerate(all_inputs):
            placeholder = input_field.get_attribute('placeholder') or input_field.get_attribute('aria-label') or 'No label'
            field_type = input_field.get_attribute('type')
            print(f"Field {i+1}: {field_type} - {placeholder}")
        
        # Fill fields in the exact order they appear: Name, Email, Address, Phone, Comments
        field_data = [name, email, address, phone, comments]
        field_names = ["Name", "Email", "Address", "Phone", "Comments"]
        
        for i, (data, input_field, field_name) in enumerate(zip(field_data, all_inputs, field_names)):
            if data and i < len(all_inputs):
                input_field.clear()
                input_field.send_keys(data)
                print(f"✓ {field_name} field filled with: {data[:20]}...")
            elif i < len(all_inputs):
                print(f"- {field_name} field skipped (no data provided)")
        
        print(f"Processed {len(all_inputs)} fields total")
        
        print("Form filled successfully!")
        
        # Ask if user wants to submit
        submit_choice = input("\nDo you want to submit the form? (y/n): ").lower().strip()
        
        if submit_choice == 'y':
            # Find and click the submit button
            try:
                submit_button = driver.find_element(By.CSS_SELECTOR, "span[jsname='V67aGc']")
                submit_button.click()
                print("Form submitted successfully!")
            except:
                print("Could not find submit button. You may need to submit manually.")
        else:
            print("Form filled but not submitted. You can review and submit manually.")
        
        # Keep browser open for a few seconds so user can see the result
        print("Keeping browser open for 5 seconds...")
        time.sleep(5)
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have Chrome browser installed and try again.")
    
    finally:
        # Close the browser
        try:
            driver.quit()
            print("Browser closed.")
        except:
            pass

# Run the program
if __name__ == "__main__":
    fill_survey()


# 04 Automate your browser to scrape this jobs page: https://people.bamboohr.com/careers
""" 
    Make a program that:
        1. Opens the browser
        2. Navigates to the jobs page URL
        3. Scrapes the jobs page
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def scrape_jobs():
    print("Job Scraper Program")
    print("This program will open your browser and scrape job listings from the BambooHR careers page.")
    print("Make sure you have Chrome browser installed!")
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        # Start the browser
        print("\nOpening browser...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://people.bamboohr.com/careers")
        
        # Wait for the page to load
        print("Waiting for page to load...")
        time.sleep(5)
        
        print("Scraping job information...")
        
        # Look for job listings - these are common selectors for job sites
        job_elements = []
        
        # Try different common selectors for job listings
        selectors_to_try = [
            ".job-listing",
            ".job-item", 
            ".position",
            "[data-testid*='job']",
            ".career-item",
            "article",
            ".job-card"
        ]
        
        for selector in selectors_to_try:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    job_elements = elements
                    print(f"Found {len(elements)} job listings using selector: {selector}")
                    break
            except:
                continue
        
        # If no specific job elements found, get all text content
        if not job_elements:
            print("No specific job elements found. Getting all page content...")
            page_content = driver.find_element(By.TAG_NAME, "body").text
            print(f"Page loaded successfully! Found {len(page_content)} characters of content.")
            print("\n" + "="*50)
            print("PAGE CONTENT:")
            print("="*50)
            print(page_content[:1000] + "..." if len(page_content) > 1000 else page_content)
            print("="*50)
        else:
            # Extract job information
            jobs = []
            for i, job_element in enumerate(job_elements[:10]):  # Limit to first 10 jobs
                try:
                    job_text = job_element.text.strip()
                    if job_text and len(job_text) > 10:  # Only include substantial content
                        jobs.append(job_text)
                except:
                    continue
            
            if jobs:
                print(f"\nFound {len(jobs)} job listings:")
                print("="*50)
                for i, job in enumerate(jobs, 1):
                    print(f"\nJOB {i}:")
                    print("-" * 30)
                    print(job)
                    print("-" * 30)
            else:
                print("No job content could be extracted.")
        
        # Keep browser open for a few seconds so user can see the result
        print("\nKeeping browser open for 10 seconds so you can see the page...")
        time.sleep(10)
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have Chrome browser installed and try again.")
    
    finally:
        # Close the browser
        try:
            driver.quit()
            print("Browser closed.")
        except:
            pass

# Run the job scraper
if __name__ == "__main__":
    scrape_jobs()


# 05 Make a website showing the wave height in Nazare
""" 
    Make a program that:
        1. Gets the wave height in Nazare
        2. Creates a website showing the wave height
"""

import requests
import json

def get_wave_height():
    """Gets the current wave height in Nazaré from the World Weather API"""
    
    # API key and location
    api_key = "WorldWeather"
    location = "Nazaré,Portugal"
    
    # API URL for marine weather
    url = f"https://api.worldweatheronline.com/premium/v1/marine.ashx"
    
    # Parameters for the API request
    params = {
        'key': api_key,
        'q': location,
        'format': 'json',
        'fx': 'no',
        'cc': 'no',
        'mca': 'yes'
    }
    
    try:
        # Make the API request
        response = requests.get(url, params=params)
        data = response.json()
        
        # Extract wave height from the response
        if 'data' in data and 'weather' in data['data']:
            weather = data['data']['weather'][0]
            hourly = weather['hourly'][0]
            wave_height = hourly['swellHeight_miles']
            return float(wave_height)
        else:
            return "No data available"
            
    except Exception as e:
        return f"Error: {str(e)}"

def create_website(wave_height):
    """Creates a simple HTML website showing the wave height"""
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Nazaré Wave Height</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f0f8ff;
                text-align: center;
                padding: 50px;
            }}
            .container {{
                background-color: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                max-width: 500px;
                margin: 0 auto;
            }}
            h1 {{
                color: #2c3e50;
                margin-bottom: 30px;
            }}
            .wave-info {{
                font-size: 24px;
                color: #3498db;
                margin: 20px 0;
            }}
            .location {{
                color: #7f8c8d;
                font-size: 18px;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌊 Nazaré Wave Report</h1>
            <div class="wave-info">
                Current Wave Height: {wave_height} meters
            </div>
            <div class="location">
                Location: Nazaré, Portugal
            </div>
        </div>
    </body>
    </html>
    """
    
    # Save the HTML to a file
    with open('wave_height.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Website created! Open 'wave_height.html' in your browser to see the wave height.")

def main():
    """Main program that gets wave height and creates the website"""
    print("Getting wave height data from Nazaré...")
    
    # Get the wave height
    wave_height = get_wave_height()
    
    print(f"Current wave height in Nazaré: {wave_height} meters")
    
    # Create the website
    create_website(wave_height)

if __name__ == "__main__":
    main()