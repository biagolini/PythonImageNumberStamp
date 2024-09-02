# Import libraries
import os
import requests
from PIL import Image, ImageDraw, ImageFont
# Import configs
import config as cf

# Function to download the font
def download_font(url, output_filename):
    response = requests.get(url)
    if response.status_code == 200: 
        css_content = response.text
        font_url_prefix = "https://fonts.gstatic.com/s/roboto/v30/"
        font_url_suffix = ".ttf"
        font_partial_path = css_content.split('url(')[1].split(')')[0].replace('\'', '')
        font_download_url = font_url_prefix + font_partial_path.split('/')[-1]
        font_response = requests.get(font_download_url)
        if font_response.status_code == 200:
            with open(output_filename, 'wb') as font_file:
                font_file.write(font_response.content)
            print(f"Font downloaded and saved as {output_filename}")
        else:
            print("Error downloading the font.")
    else:
        print("Error accessing the font CSS.")

# Ensure the output directories exist
if not os.path.exists(cf.output_path):
    os.makedirs(cf.output_path)
if not os.path.exists(cf.font_path):
    os.makedirs(cf.font_path)

# Download the font
if not os.path.exists(cf.font_file):
    download_font(cf.font_url, cf.font_file)

# Load the base image
base_image = Image.open(cf.base_image_path)

# Load the downloaded font
try:
    font = ImageFont.truetype(cf.font_file, cf.font_size)
except IOError:
    print(f"Could not load the font: {cf.font_file}")
    font = ImageFont.load_default()

# Function to add number and save the image
def add_number_to_image(image, number, font, output_path, position_x, position_y):
    draw = ImageDraw.Draw(image)
    text = str(number)
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    image_width, image_height = image.size
    position = (
        int((image_width - text_width) * position_x / 100),
        int((image_height - text_height) * position_y / 100)
    )
    
    draw.text(position, text, font=font, fill=cf.border_color)
    draw.text(position, text, font=font, fill=cf.font_color, stroke_width=2, stroke_fill=cf.border_color)
    
    output_filename = f"{output_path}{number}.jpg"
    image.save(output_filename)
    print("Image " + str(number) + " successfully generated!")

# Generate the images
for i in range(cf.start_number, cf.end_number + 1):
    image_copy = base_image.copy()
    add_number_to_image(image_copy, i, font, cf.output_path, cf.position_x, cf.position_y)


