# Use an official Node.js base image with Python preinstalled
FROM node:18

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python

# Set working directory
WORKDIR /app

# Copy Node.js files
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy Python requirements and Python files
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy rest of the project files
COPY . .

# Expose port (use the same as in your server.js)
EXPOSE 5000

# Start your server
CMD ["node", "server.js"]
