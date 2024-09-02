# Configuration Section for image generation
base_image_path = 'img.jpg'
output_path = 'img/'
font_path = 'fonts/'
start_number = 1
end_number = 15
font_size = 50
font_url = 'https://fonts.googleapis.com/css2?family=Roboto:wght@700&display=swap'
font_file = f'{font_path}Roboto-Bold.ttf'
font_color = "black"  # or HEX code like #000000
border_color = "white"# or HEX code like "#FFFFFF" 
# Position control (percentage relative to image dimensions)
position_x = 50  # Horizontal position percentage (0 = left, 50 = center, 100 = right)
position_y = 35  # Vertical position percentage (0 = top, 50 = center, 100 = bottom)

# Configuration Section for add tags to S3 objects
bucket_name = 'YOUR-S3-BUCKET-NAME'
bucket_path = 'img/' 
user_defined_metadata = {
    "author": "Your Name",
    "description": "Generated image with a number overlay"
}
system_defined_metadata = {
    "Cache-Control": "max-age=15"
}