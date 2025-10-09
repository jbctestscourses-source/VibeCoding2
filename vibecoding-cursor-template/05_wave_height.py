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
