import getopt
import glob
import os
import re
import sys

import yt_dlp

ydl_opts = { "format": "mp4", "quiet": True }

def extract_leading_number(s):
    match = re.match(r"(\d+)", s)
    return int(match.group(1)) if match else 0
    
def escape_filename(filename):
    return ''.join(['\\' + char if not char.isalnum() else char for char in filename])

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "hxko:")
    if len(args) < 1:
      print("Usage: extract_chapters.py [video_url]")
      exit()
    else:
      url = args[0]

    ydl_opts['outtmpl'] = os.path.join(os.getcwd(), "%(title)s.%(ext)s") 

    # use yt-dlp library to get video/metadata
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # extract metadata to check for presence of chapters before downloading
        info_dict = ydl.extract_info(url, download=False)

        if "chapters" not in info_dict or not info_dict["chapters"]:
            print("This video does not have chapters")
            exit()

        title = info_dict["title"]
        ext = info_dict["ext"]

        filename = f"{title}.{ext}"

        ydl.download([url])

        chapterdict = info_dict["chapters"]
        order = []

        # allow user to rearrange chapters by typing in their indices
        # in the order they prefer
        while len(chapterdict) != 0:
          for idx, chapter in enumerate(chapterdict):
            print(idx, chapter["title"])
          ind = input("Type the index of the chapter you would like to include next: \n")
          if not ind.isdigit():
            print("Index must be a positive whole number. Pick again.")
            continue
          if int(ind) >= len(chapterdict):
            print("This index does not exist in the list. Pick again.")
            continue
          order.append(chapterdict[int(ind)])
          del chapterdict[int(ind)]

        # with the given order, extract each chapter from the original
        # video into its own mp4 file using ffmpeg.
        # append the index to the filename for later sorting
        for idx, chapter in enumerate(order):
          start_time = chapter["start_time"]
          end_time = chapter["end_time"]
          chapter_title = chapter["title"]
          cmd = f"""ffmpeg -ss {start_time} -i "{title}.{ext}" -to {end_time} -codec copy -copyts \"{idx}-{chapter_title}.{ext}\""""
          os.system(cmd)
        
        # delete the original full video file
        os.remove(filename)
          
        files = glob.glob(os.path.join(os.getcwd(), '*.mp4'))
        files.sort(key=lambda x: extract_leading_number(os.path.basename(x)))

        # write all mp4 filenames to a text file that we can
        # later pass into ffmpeg to concatenate
        with open('list.txt', 'w') as file:   
          for filepath in files:
            filename = os.path.basename(filepath)
            escaped = escape_filename(filename)
            file.write(f"file {escaped}\n")

        # re-concatenate chapters into one video file
        os.system("ffmpeg -safe 0 -f concat -i list.txt -c copy output.mp4")

        # delete all video chunks and order list file
        os.system("find . -type f -name \"*.mp4\" ! -name \"output.mp4\" -exec rm {} \;")
        os.system("rm list.txt")
    
    print("Done!")