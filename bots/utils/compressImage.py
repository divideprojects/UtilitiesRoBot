from PIL import Image


async def compress_image(image_path: str):
    image_name = image_path.split("/")[-1]
    new_filename = f"compressed_{image_name}"

    pic = Image.open(image_path)
    pic = pic.resize(pic.size, Image.LANCZOS)
    pic.save(
        new_filename,
        optimize=True,
        quality=25,
    )
    return new_filename
