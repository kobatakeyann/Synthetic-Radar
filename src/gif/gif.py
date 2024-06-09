import os
from glob import glob
from PIL import Image

def convert_jpg_to_gif(parent_path:str,saved_dir_path:str,gif_name:str) -> None:
    img_array = []
    for img_filename in sorted(glob(f"{parent_path}/*.jpg")):
        img = Image.open(img_filename)
        img.thumbnail((1200,800))
        img_array.append(img)

        out_path = os.path.join(saved_dir_path,gif_name)

    img_array[0].save(out_path ,save_all=True, append_images=img_array[1:], optimize=True, duration=90, loop=0)
