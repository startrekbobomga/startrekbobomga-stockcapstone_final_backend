# Use an official Node.js image with Debian base
FROM node:18

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python

# Set the working directory
WORKDIR /app

# Copy Node.js dependencies
COPY package*.json ./
RUN npm install

# Copy Python requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose port
EXPOSE 5000

# Start the Node.js server
CMD ["node", "server.js"]
