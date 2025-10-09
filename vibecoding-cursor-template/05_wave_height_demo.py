import requests

def get_demo_wave_height():
    """Returns sample wave height data for demonstration"""
    # This is demo data - in real life, this would come from the API
    return 15.2  # meters - typical for big waves in Nazaré!

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
            .note {{
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 5px;
                padding: 15px;
                margin-top: 20px;
                font-size: 14px;
                color: #856404;
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
            <div class="note">
                📝 This is demo data. The real program connects to the World Weather API to get live wave heights!
            </div>
        </div>
    </body>
    </html>
    """
    
    # Save the HTML to a file
    with open('wave_height_demo.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Demo website created! Open 'wave_height_demo.html' in your browser to see the wave height.")

def main():
    """Main program that shows how the wave height website works"""
    print("Creating demo wave height website for Nazaré...")
    
    # Get demo wave height
    wave_height = get_demo_wave_height()
    
    print(f"Demo wave height in Nazaré: {wave_height} meters")
    
    # Create the website
    create_website(wave_height)
    
    print("\n🌊 What this program does:")
    print("1. Gets wave height data (from API in real version)")
    print("2. Creates a beautiful website showing the data")
    print("3. You can open the HTML file in any web browser")

if __name__ == "__main__":
    main()
