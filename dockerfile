# Use official Node.js base image (Debian-based)
FROM node:18

# Install system dependencies: Python, pip, Chromium, ChromeDriver
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv chromium chromium-driver && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables for Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH=$PATH:/usr/bin

# Set working directory
WORKDIR /app

# Copy Node.js dependencies
COPY package*.json ./
RUN npm install

# Copy Python requirements and install in virtual env
COPY requirements.txt ./
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Copy remaining files
COPY . .

# Expose app port
EXPOSE 5000

# Start server
CMD ["node", "server.js"]
