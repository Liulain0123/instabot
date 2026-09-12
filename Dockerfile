# 使用輕量級的 Python 3.11 鏡像
FROM python:3.11-slim

# 安裝系統依賴 (FFmpeg 用於處理 IG 影片)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案檔案
COPY . .

# 啟動機器人
CMD ["python", "main.py"]
