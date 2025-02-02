from config import Config
from helpers.get_link import get_link
from helpers.magnet import Magnet
from helpers.aandu import uploadtg,download
from helpers.inlin import inline_keyboard2,inline_keyboard
from helpers.video import screenshots
from DB.video import DB,Video
from DB.admin import Admin
import random,string
import time
import os
import asyncio
db= DB()
admin = Admin()

text = '''
🎥 {title}

📸 Screenshots: https://h.migna155.workers.dev/ss/{id}

🎥 Watch: https://h.migna155.workers.dev/v/{id}
'''

async def start_worker(message, client):
    if admin.get_worker():
        xvideo = await get_link()
        if xvideo:
            await message.edit(f"Video found: {xvideo.title}", reply_markup=inline_keyboard2)
            magnet = Magnet()
            magnet.upload_torrent(xvideo.link)
            if magnet.check_torrent():
                 title , link = magnet.select_File(magnet.account.listContents())
                 if title:
                    await download(message,link,inline_keyboard2)
                    await message.edit("Now generating screenshots...", reply_markup=inline_keyboard2)
                    video_info,list_screenshots = await screenshots(client)
                    start_time = time.time()
                    vid = await client.send_video(video="video.mp4",thumb="thumbnail.jpg",duration=video_info.get("duration"),width=video_info.get("width"),height=video_info.get("height"),supports_streaming = True,chat_id=Config.CHANNEL_ID,caption=xvideo.title,file_name=title,progress=uploadtg,progress_args=(message,start_time,inline_keyboard2))
                    os.remove("thumbnail.jpg")
                    video = Video(
                        id = ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
                        title = xvideo.title,
                        telegramid=vid.id,
                        size = os.path.getsize("video.mp4"),
                        screenshots = list_screenshots
                    )
                    db.add_video(video)
                    await message.edit("Video uploaded successfully", reply_markup=inline_keyboard2)
                    await asyncio.sleep(5)
                    photo = random.choice(os.listdir("ss"))

                    await client.send_photo(chat_id=Config.MAIN_CHANNEL,
                                            photo=f"SS/{photo}",
                                            caption=text.format(title=video.title,id=video.id)
                                            )
                    for file in os.listdir("ss"):os.remove(f"ss/{file}")
                    os.remove("video.mp4")
                    await asyncio.sleep(15)
                    await message.edit("Starting worker again...", reply_markup=inline_keyboard2)
                    await start_worker(message, client)
        else:
            await message.edit("No video found in rss feed", reply_markup=inline_keyboard2)

            await asyncio.sleep(Config.SLEEP_TIME)
            await message.edit("Starting worker again...", reply_markup=inline_keyboard2)
            await start_worker(message, client)
    else:
        await message.edit("Worker is not enabled", reply_markup=inline_keyboard)

    
