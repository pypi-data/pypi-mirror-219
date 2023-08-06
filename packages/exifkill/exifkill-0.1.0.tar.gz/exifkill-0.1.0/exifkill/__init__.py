from PIL import Image


def drop_exif(input_path: str, output_path: str):
    image = Image.open(input_path)
    data = list(image.getdata())
    image2 = Image.new(image.mode, image.size)
    image2.putdata(data)
    image2.save(output_path)
