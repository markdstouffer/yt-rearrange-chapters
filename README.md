# Rearrange YouTube Chapters

This is a project to allow users to download a YouTube video from its URL
and rearrange its chapters to an order suitable to them.

## Usage

`python3 rearrange_chapters.py [url]`

The script will then check the chapter data. If there are no marked chapters, the script will exit (many other projects can be used to just download YouTube videos). Otherwise, it will list out the titles of each chapter, along with an index.

You will then be prompted to continue entering index numbers in the order you prefer, until all chapters
have been accounted for. The final file will be found in this working directory, titled `output.mp4`.

## Prerequisites

- Python
- [yt-dlp](https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#installation)
- [ffmpeg](https://ffmpeg.org/)

### Credits

Some of the code has been adapted from a Gist written by telugu-boy, found [here](https://gist.github.com/telugu-boy/a2ca5b99d501e6f5f295333537a2a849).
