from pyrogram import Client
from config import Config
from fastapi import FastAPI, Request
from uvicorn import Server as UvicornServer, Config as UvicornConfig


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

class Bot(Client):
    def __init__(self):
        super().__init__("my_account",
             api_id=Config.API_ID,
             api_hash=Config.API_HASH,
             bot_token=Config.BOT_TOKEN,
             plugins=dict(root="plugins")
             )
    async def start(self):
        await super().start()
        await self.send_message(int(Config.LOG_GROUP), "Bot started")
        
    async def stop(self):
        await super().stop()
        await self.send_message(int(Config.LOG_GROUP), "Bot stopped")
        
    async def restart(self):
        await self.stop()
        await self.start()
        await self.send_message(int(Config.LOG_GROUP), "Bot restarted")


server = UvicornServer (
    UvicornConfig (
        app=app,
        host="0.0.0.0",
        port=8000
    )
)

if __name__ == "__main__":
    bot = Bot()
    bot.loop.create_task(server.serve())
    bot.run()
