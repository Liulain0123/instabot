import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp
import os
import asyncio
import re
import urllib.request
import logging
from dotenv import load_dotenv

# --- 日誌設定 ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('InstaBot')

# 加載 .env 文件
load_dotenv()

# --- 設定區 ---
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    logger.error("找不到 DISCORD_TOKEN！請檢查 .env 檔案或系統環境變數。")
    exit(1)

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guild_messages = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        logger.info(f"已同步斜槓指令 (Slash Commands) 為 {self.user}")

bot = MyBot()

# --- Instagram 預覽邏輯 ---
def normalize_ig_url(url):
    return re.sub(r'instagram\.com/reel/', 'instagram.com/reels/', url, flags=re.IGNORECASE)

def fetch_ig_caption(url):
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode('utf-8')
            match = re.search(r'<meta property="og:description" content="([^"]+)">', html)
            if match:
                return match.group(1).replace('&quot;', '"').replace('&amp;', '&')
    except Exception:
        pass
    return ""

def get_ig_info(url):
    normalized_url = normalize_ig_url(url)
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    ]
    for ua in user_agents:
        ydl_opts = {'quiet': True, 'no_warnings': True, 'format': 'best', 'user_agent': ua, 'nocheckcertificate': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(normalized_url, download=False)
                entry = info['entries'][0] if 'entries' in info else info
                media_url = entry.get('url')
                if not media_url and entry.get('formats'):
                    media_url = entry['formats'][-1].get('url')
                if not media_url:
                    media_url = entry.get('thumbnail')
                ext = entry.get('ext', 'jpg')
                if media_url and ('video' in media_url or 'mp4' in media_url):
                    ext = 'mp4'
                description = entry.get('description', '') or fetch_ig_caption(normalized_url)
                return media_url, ext, description
        except Exception:
            continue
    return None, None, None

async def download_video(url, filename):
    def sync_download():
        ydl_opts = {
            'outtmpl': filename,
            'quiet': True,
            'no_warnings': True,
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    await asyncio.to_thread(sync_download)

@bot.tree.command(name="ig", description="獲取 Instagram 貼文預覽")
@app_commands.describe(url="請貼上 Instagram 貼文連結")
async def ig_preview(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    normalized_url = normalize_ig_url(url)
    media_url, ext, caption = await asyncio.to_thread(get_ig_info, normalized_url)
    text_content = f"{caption}\n\n[點擊查看原貼文]({normalized_url})" if caption else f"[點擊查看原貼文]({normalized_url})"
    if media_url:
        if ext in ['mp4', 'm4v', 'mov'] or 'video' in media_url:
            filename = f"temp_video_{interaction.id}.mp4"
            try:
                await download_video(media_url, filename)
                msg = f"🎥 **Instagram 影片**\n{text_content}"
                file = discord.File(filename)
                await interaction.followup.send(content=msg, file=file)
            except Exception as e:
                logger.error(f"Upload error: {e}")
                proxy_url = normalized_url.replace("instagram.com", "kkinstagram.com")
                await interaction.followup.send(f"🎥 **影片預覽 (下載失敗)**\n{text_content}\n\n{proxy_url}")
            finally:
                if os.path.exists(filename):
                    os.remove(filename)
            return
        embed = discord.Embed(title="📸 Instagram 圖片預覽", description=text_content, color=discord.Color.from_rgb(225, 48, 108))
        embed.set_image(url=media_url)
        await interaction.followup.send(embed=embed)
    else:
        proxy_url = normalized_url.replace("instagram.com", "kkinstagram.com")
        caption = fetch_ig_caption(normalized_url)
        text_content = f"{caption}\n\n[點擊查看原貼文]({normalized_url})" if caption else f"[點擊查看原貼文]({normalized_url})"
        embed = discord.Embed(title="📸 Instagram 圖片預覽 (代理模式)", description=text_content, color=discord.Color.from_rgb(225, 48, 108))
        embed.set_image(url=proxy_url)
        await interaction.followup.send(embed=embed)

bot.run(TOKEN)
