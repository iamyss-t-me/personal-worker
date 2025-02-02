import subprocess
import json
import os
import imageio
from config import Config
from DB.video import Screenshot
import asyncio
from PIL import Image
import random
import io
config = Config()
def capture_frame(video_path, timestamp, output_filename):
    vid = imageio.get_reader(video_path, 'ffmpeg')
    frame_num = int(vid.get_meta_data()['fps'] * timestamp)
    frame = vid.get_data(frame_num)
    imageio.imwrite(output_filename, frame)

def get_video_info(input_filename):
    command = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", input_filename]
    output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
    data = json.loads(output)

    video_info = None
    for stream in data.get("streams", []):
        if stream.get("codec_type") == "video":
            video_info = {
                "width": stream.get("width"),
                "height": stream.get("height"),
                "duration": float(data["format"]["duration"])
            }
            break
    return video_info


def seconds_to_hms(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"


async def screenshots(client):
    if not os.path.exists("ss"):os.makedirs("ss")
    video_info = get_video_info("video.mp4")
    duration = video_info.get("duration")
    n = int(duration/int(Config.SCREENSHOTS_COUNT))
    images = []
    for i in range(1,int(Config.SCREENSHOTS_COUNT)+1):
        if i/3 == 0:await asyncio.sleep(4)
        capture_frame("video.mp4",n*i,f"ss/{i}.jpg")
        image = await client.send_photo(int(Config.CHANNEL_ID),f"ss/{i}.jpg")
        await asyncio.sleep(1)
        images.append(Screenshot(id=image.id,url=f"ss/{i}.jpg",timestamp=seconds_to_hms(i*10)))
        thumbnail = random.choice(os.listdir("ss"))
    create_thumbnail(f"SS/{thumbnail}")
    return video_info,images



def create_thumbnail(input_image_path):
    with Image.open(input_image_path) as img:
        img.thumbnail((320, 320))
        img.save("thumbnail.jpg", "JPEG", quality=85)
        while os.path.getsize("thumbnail.jpg") > 200 * 1024:
            quality = int(img.info.get('quality', 85)) - 5
            img.save("thumbnail.jpg", "JPEG", quality=quality)
        

