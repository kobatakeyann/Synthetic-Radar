from glob import glob

from constant import GIF_INTERVAL_TIME
from PIL import Image


def make_gif_from_imgs(img_dir_path: str, saved_gif_path: str) -> None:
    img_array = []
    for img_filename in sorted(glob(f"{img_dir_path}/*.jpg")):
        img = Image.open(img_filename)
        img.thumbnail((1200, 800))
        img_array.append(img)
    img_array[0].save(
        saved_gif_path,
        save_all=True,
        append_images=img_array[1:],
        optimize=True,
        duration=GIF_INTERVAL_TIME,
        loop=0,
    )
