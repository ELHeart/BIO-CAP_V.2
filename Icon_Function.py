from PIL import Image


def convert_image_to_icon(image_path, icon_path, icon_sizes=(16, 32, 48, 64, 128, 256)):
    """
    Convert an image to an ICO file with specified sizes.

    :param image_path: The path to the input image.
    :param icon_path: The path where the ICO file will be saved.
    :param icon_sizes: A tuple of sizes (in pixels) for the icon.
    """
    # Open the image file
    with Image.open(image_path) as image:
        # Convert the image to RGBA format (required for ICO files)
        image = image.convert('RGBA')

        # Generate the icon with multiple sizes
        icon_sizes = [(size, size) for size in icon_sizes]
        image.save(icon_path, format='ICO', sizes=icon_sizes)


# Example usage:
convert_image_to_icon(r'C:\Users\el_he\Desktop\BIO-CAP_V.2\BIOCAP.png',
                      r'C:\Users\el_he\Desktop\BIO-CAP_V.2\BIOCAP.ico')
