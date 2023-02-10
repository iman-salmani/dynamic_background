#!/usr/bin/python
import os, subprocess, argparse, random
from time import sleep, localtime


class Daemon:
    backgrounds_dir = os.path.join(os.getenv("HOME"), "Pictures", "Backgrounds")
    light_dir = os.path.join(backgrounds_dir, "Light")
    dark_dir = os.path.join(backgrounds_dir, "Dark")

    def __init__(self, interval) -> None:
        light_backgrounds = self.get_backgrounds(self.light_dir)
        dark_backgrounds = self.get_backgrounds(self.dark_dir)

        light_i = 0
        dark_i = 0
        while True:
            # Set schema
            hour = localtime().tm_hour
            if hour < 6 and hour > 18:
                os.system(
                    "gsettings set org.gnome.desktop.interface color-scheme prefer-dark"
                )
            else:
                os.system(
                    "gsettings set org.gnome.desktop.interface color-scheme default"
                )

            # Set background
            if self.is_dark():
                key = "picture-uri-dark"
                path = dark_backgrounds[dark_i]

                dark_i += 1
                if dark_i == len(dark_backgrounds):
                    dark_i = 0
            else:
                key = "picture-uri"
                path = light_backgrounds[light_i]

                light_i += 1
                if light_i == len(light_backgrounds):
                    light_i = 0

            os.system(f"gsettings set org.gnome.desktop.background {key} {path}")

            sleep(interval)

    def is_dark(self):
        color_scheme = str(
            subprocess.run(
                ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
                stdout=subprocess.PIPE,
            ).stdout
        )
        if color_scheme.find("dark") != -1:
            return True
        return False

    def get_backgrounds(self, dir_path):
        backgrounds = []
        files = os.listdir(dir_path)
        random.shuffle(files)
        for file in files:
            path = os.path.join(dir_path, file)
            # TODO: check file type
            if os.path.isfile(path):
                backgrounds.append(path)
        return backgrounds


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(prog="Dynamic Background")
    argparser.add_argument("-i", "--interval", type=int, help="Refresh interval")
    args = argparser.parse_args()
    if not args.interval:
        args.interval = 30 * 60
    Daemon(args.interval)
