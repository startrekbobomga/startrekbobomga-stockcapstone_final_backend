# Use an official Node.js image (includes Debian)
FROM node:18

# Install Python & venv support
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    ln -s /usr/bin/python3 /usr/bin/python

# Set working directory
WORKDIR /app

# Copy and install Node.js dependencies
COPY package*.json ./
RUN npm install

# Copy Python requirements
COPY requirements.txt ./

# Set up Python virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies inside the venv
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port
EXPOSE 5000

# Start Node.js server
CMD ["node", "server.js"]
