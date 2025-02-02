import requests
import time
from helpers.helper import size_format,convert,progress_bar
from datetime import datetime
from pyrogram.errors import MessageNotModified
tex = '''
**📥 Downloading To Server**
`{}`
`Percentage` : `{}%`
`Total` : `{}`
`Downloaded` : `{}`
`Remaining` : `{}`
`Speed` : `{}/s`
`ETA` : `{}`
'''

async def download(message,url: str,inline_keyboard2) -> None:
    r = requests.head(url, allow_redirects=True)
    file_size = int(r.headers.get('content-length', 0))
    r = requests.get(url, stream=True)
    start_time = time.time()
    elapsed_time = time.time()
    downloaded_size = 0
    with open("video.mp4", 'wb') as f:
        for chunk in r.iter_content(chunk_size=2048):
            if chunk:
                f.write(chunk)
                downloaded_size += len(chunk)
                if time.time() - elapsed_time > 7:
                    elapsed_time = time.time()
                    speed = downloaded_size / (time.time() - start_time)
                    eta = (file_size - downloaded_size) / speed if speed > 0 else 0
                    percent = f"{(downloaded_size / file_size) * 100:.2f}"
                    text = tex.format(progress_bar((downloaded_size / file_size) * 100),percent, size_format(file_size), size_format(downloaded_size), size_format(file_size - downloaded_size), size_format(speed), convert(eta))
                    try:
                        await message.edit(text+f"\n\n🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", reply_markup=inline_keyboard2)
                    except MessageNotModified:
                        pass
        await message.edit("Downloaded Successfully", reply_markup=inline_keyboard2)
utex = '''
** 📤 Uploading to Telegram**
`{}`
`Percentage` : `{}%`
`Total` : `{}`
`Uploaded` : `{}`
`Remaining` : `{}`
`Speed` : `{}/s`
`ETA` : `{}`
'''

elapsed_time = 0
async def uploadtg(current,total,message,start_time,inline_keyboard2):
    percent = f"{(current / total) * 100:.2f}"
    global elapsed_time
    if time.time()-elapsed_time > 5:
        speed = current / (time.time() - start_time)
        eta = (total - current) / speed if speed > 0 else 0
        text = utex.format(progress_bar((current / total) * 100),percent, size_format(total), size_format(current), size_format(total - current), size_format(speed), convert(eta))
        try:
            await message.edit(text, reply_markup=inline_keyboard2)
        except MessageNotModified:
            pass
        elapsed_time = time.time()
        