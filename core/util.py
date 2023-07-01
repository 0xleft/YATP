import os

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
    resized_image = image.resize((new_width, new_height))

    # Save the resized image with reduced quality
    resized_image.save(output_path, optimize=True)

def convert_images(selected_folder):
    try:
        os.mkdir(selected_folder + "/small")
    except FileExistsError:
        pass

    for file in os.listdir(selected_folder):
        if file.endswith(".jpg") or file.endswith(".png"):
            downscale_image(selected_folder + "/" + file, selected_folder + "/small/small_" + file, 700)