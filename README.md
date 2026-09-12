# 📸 InstaBot - Instagram Reels 預覽機器人


InstaBot 是一個精簡且高效的 Discord 機器人，專為 **Instagram Reels** 的快速預覽而設計。它能將 IG Reels 影片直接下載並上傳至 Discord 頻道，讓使用者無需跳轉頁面即可觀看。

## ✨ 主要功能

### 🎥 Reels 影片預覽
- **`/ig [連結]`**：貼上 Instagram Reels 連結，機器人會執行以下操作：
  - **直接下載**：嘗試抓取影片原檔並直接上傳至 Discord。
  - **代理模式 (保底方案)**：若伺服器 IP 被 Instagram 暫時封鎖，機器人會自動提供一個代理連結，確保您依然可以觀看內容。

## 🚀 快速部署 (Railway)

### 1. 準備 GitHub
- 建立一個 **Public (公開)** 的 GitHub 儲存庫。
- 上傳以下 6 個檔案：
  - `main.py`
  - `requirements.txt`
  - `Dockerfile`
  - `.gitignore`
  - `README.md`
  - `LICENSE`

### 2. Railway 設定
- 在 Railway 中連結該 GitHub 儲存庫。
- 在 **Variables** 中新增：
  - `DISCORD_TOKEN`: 您的機器人 Token。
- 在 **Settings** 中確認 Builder 為 `Dockerfile`。

## 📦 技術棧
- **語言**: Python 3.11
- **框架**: `discord.py`
- **提取**: `yt-dlp`
- **處理**: `FFmpeg`
- **部署**: Docker $\rightarrow$ Railway

## 🛡️ 安全與開源聲明
本專案採取 **MIT License** 授權。為了確保使用者帳號的絕對安全，本版本**不使用任何私人 Cookie**。這意味著：
- 帳號 100% 安全，無洩漏風險。
- 由於 Instagram 的反爬蟲機制，部分內容可能會觸發代理模式，這是在不使用憑證情況下的最佳穩定方案。

---
*本專案旨在提供便捷的媒體預覽體驗，請在遵守 Discord 與 Instagram 服務條款的前提下使用。*
