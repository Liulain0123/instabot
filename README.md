# 📸 InstaBot - Instagram 預覽機器人

InstaBot 是一個簡單而高效的 Discord 機器人，專門用於在 Discord 頻道中快速預覽 Instagram 的貼文與 Reels。

## ✨ 功能
- **`/ig [網址]`**：貼上 Instagram 連結，機器人會自動抓取內容。
  - **影片 (Reels/Video)**：自動下載並上傳至 Discord。
  - **圖片**：以精美 Embed 形式顯示圖片預覽。
  - **描述**：自動抓取貼文的文字描述。

## 🚀 快速部署 (Railway)

### 1. 準備 GitHub
- 建立一個 **Public (公開)** 的 GitHub 儲存庫。
- 上傳以下檔案：
  - `main.py`
  - `requirements.txt`
  - `Dockerfile`
  - `.gitignore`
  - `README.md`

### 2. Railway 設定
- 在 Railway 連結該 GitHub 儲存庫。
- 在 **Variables** 中新增：
  - `DISCORD_TOKEN`: 您的機器人 Token。
- 在 **Settings** 中確認 Builder 為 `Dockerfile`。

## 📦 技術棧
- **語言**: Python 3.11
- **框架**: `discord.py`
- **提取**: `yt-dlp`
- **處理**: `FFmpeg`
- **部署**: Docker $\rightarrow$ Railway

---
*本專案為開源版本，不使用私人 Cookie 以確保帳號安全性。*
