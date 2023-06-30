from PIL import Image

# downscale the image with the maximum size indicated by the third parameter
def downscale_image(input_path, output_path, max_size):
    # Open the image
    image = Image.open(input_path)

    ratio = image.size[0] / image.size[1]

    if image.width <= max_size and image.height <= max_size:
        new_width = image.width
        new_height = image.height
    else:
        if image.width > max_size:
            new_width = max_size
            new_height = int(new_width / ratio)
        else:
            new_height = max_size
            new_width = int(new_height * ratio)

    # Resize the image
    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

    # Save the resized image with reduced quality
    resized_image.save(output_path, optimize=True)
