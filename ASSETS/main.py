import os
import random
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import InputFile
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.token import validate_token

from aiohttp import web

# ========== CONFIG ========== #
API_TOKEN = '7590726446:AAHWeqnxs4xJyMkyMFN9xr_avk16EPVBIVw'
validate_token(API_TOKEN)

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# ========== GRUPOS ========== #
GROUPS = {
    "-1002733177508": "@ZonaProBot",        # Novinhas e Ninfetas
    "-1002733196174": "@VaultXClubBot",     # Novinhas Nudes
    "-1002857824461": "@ObscurioBot"        # Novinhas Amadoras
}

# ========== LEGENDAS ========== #
LEGENDS = [
    "👀 Se esses você já gostou, o que tem no VIP vai te deixar maluco\n\nLibera aqui 👉 {at}",
    "😈 O grupo FREE é bom. Mas o VIP é sacanagem pura:\n🔥 Vídeos vazados do Only e Privacy\n😈 Ninfetas fazendo de tudo\n😏 Nada de repetição — só coisa nova\n\n👉 {at}",
    "⚠️ Aqui é só a superfície…\nO verdadeiro conteúdo tá num grupo que só entra quem paga — e vale cada centavo.\n\n😈 Lá não tem vídeo repetido, tem vídeo EXCLUSIVO.\n🔥 Só ninfetas, novinhas e vazados do Onlyfans e Privacy atualizados.\n\n👉 Entra aqui: {at}",
    "🔥🍭GRUPO NOVINHAS VIP🍭🔥\n\n✅ Novinhas da buceta apertada\n✅ Estudantes\n✅ Vazados do Onlyfans/Privacy\n✅ 100% Anônimo\n\nTá esperando o que? Acessa logo 😈🔥\n👉 {at}"
]

# ========== HORÁRIOS ========= #
SCHEDULE = {
    "07:30": [0, 1],
    "10:30": [2, 3],
    "13:30": [4, 5, 6],
    "17:30": [7, 8, 9],
    "20:30": [10, 11, 12],
    "23:30": [13, 14]
}

# ========== VÍDEOS ========== #
VIDEO_NAMES = [
    "WhatsApp Video 2025-07-13 at 13.40.47_1752435667130.mp4",
    "WhatsApp Video 2025-07-13 at 13.41.52_1752435667128.mp4",
    "WhatsApp Video 2025-07-13 at 13.42.06_1752435667127.mp4",
    "WhatsApp Video 2025-07-13 at 13.42.13_1752435667127.mp4",
    "WhatsApp Video 2025-07-13 at 13.42.22_1752435667126.mp4",
    "WhatsApp Video 2025-07-13 at 13.42.28_1752435667124.mp4",
    "WhatsApp Video 2025-07-13 at 13.42.34_1752435667123.mp4",
    "WhatsApp Video 2025-07-13 at 13.42.44_1752435667123.mp4",
    "WhatsApp Video 2025-07-13 at 13.42.49_1752435667122.mp4",
    "WhatsApp Video 2025-07-13 at 13.43.00_1752435667121.mp4",
    "WhatsApp Video 2025-07-13 at 13.43.05_1752435667120.mp4",
    "WhatsApp Video 2025-07-13 at 13.43.52_1752435667119.mp4",
    "WhatsApp Video 2025-07-13 at 13.43.58_1752435667118.mp4",
    "WhatsApp Video 2025-07-13 at 13.47.01_1752435667117.mp4",
    "WhatsApp Video 2025-07-13 at 16.33.50_1752435667104.mp4"
]

# ========== FUNÇÃO DE ENVIO ========= #
async def send_videos():
    while True:
        now = datetime.now().strftime('%H:%M')
        if now in SCHEDULE:
            video_indexes = SCHEDULE[now]
            for group_id, at in GROUPS.items():
                for idx in video_indexes:
                    file_path = f"attached_assets/{VIDEO_NAMES[idx]}"
                    if os.path.exists(file_path):
                        caption = random.choice(LEGENDS).replace("{at}", at)
                        try:
                            await bot.send_video(chat_id=group_id, video=InputFile(file_path), caption=caption)
                            await asyncio.sleep(4)
                        except Exception as e:
                            print(f"Erro ao enviar para {group_id}: {e}")
            await asyncio.sleep(60)
        await asyncio.sleep(20)

# ========== SERVER UPTIME ROBOT ========= #
async def handle(request):
    return web.Response(text="Bot está online.")

app = web.Application()
app.router.add_get("/", handle)

async def start_webserver():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

# ========== INICIAR BOT ========= #
async def main():
    await start_webserver()
    asyncio.create_task(send_videos())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
