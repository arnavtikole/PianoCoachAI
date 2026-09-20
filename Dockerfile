FROM python:3.11-slim

WORKDIR /app

# System dependencies needed by Audiveris and Python audio libraries
RUN apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    libasound2 \
    libfreetype6 \
    libfontconfig1 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxi6 \
    libxrandr2 \
    libxtst6 \
    libglib2.0-0 \
    libgl1 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Audiveris 5.11.0
RUN mkdir -p /usr/share/desktop-directories \
    && wget -O /tmp/audiveris.deb \
    https://github.com/Audiveris/audiveris/releases/download/5.11.0/Audiveris-5.11.0-ubuntu22.04-x86_64.deb \
    && apt-get update \
    && apt-get install -y /tmp/audiveris.deb \
    && rm /tmp/audiveris.deb \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Streamlit listens on Render's assigned port
CMD ["sh", "-c", "streamlit run app.py --server.address=0.0.0.0 --server.port=${PORT:-10000}"]