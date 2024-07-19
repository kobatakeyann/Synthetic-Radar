from configuration import TITLE_NAME
from helper.time import PaddingDatetime
from util.path import generate_path


class TextAquisition(PaddingDatetime):
    def get_title_text(self) -> str:
        title = f"{self.year}/{self.month}/{self.day} {self.hour}{self.minute}JST  {TITLE_NAME}"
        return title

    def get_save_dir(self) -> str:
        save_path = generate_path(f"/img/{self.year}/{self.month}/{self.day}")
        return save_path

    def get_save_filename(self) -> str:
        file_name = f"{self.year}{self.month}{self.day}_{self.hour}{self.minute}JST.jpg"
        return file_name

    def get_save_gifname(self) -> str:
        gif_file_name = f"{self.year}{self.month}{self.day}.gif"
        return gif_file_name

    def get_save_videoname(self) -> str:
        video_name = f"{self.year}{self.month}{self.day}.mp4"
        return video_name
