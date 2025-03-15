#!/usr/bin/env bash

# Exit on errors
set -o errexit

# Create a directory for Chrome installation
mkdir -p /opt/render/project/.render/chrome

# Download and install Chrome
echo "Downloading and Installing Chrome from https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
curl -SL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /tmp/chrome.deb
dpkg -x /tmp/chrome.deb /opt/render/project/.render/chrome

# Download and install ChromeDriver
CHROME_VERSION=$(/opt/render/project/.render/chrome/opt/google/chrome/google-chrome --version | awk '{print $3}' | cut -d'.' -f1,2)
echo "Chrome Version: $CHROME_VERSION"

# CHROME_VERSION=$(/opt/render/project/.render/chrome/opt/google/chrome/google-chrome --version | awk '{print $3}')
# CHROME_VERSION=$(/opt/render/project/.render/chrome/opt/google/chrome/google-chrome --version | awk '{print $3}' | cut -d'.' -f1,2)
# CHROME_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
# CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")

CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
echo "Downloading and installing ChromeDriver version: $CHROMEDRIVER_VERSION"
curl -SL "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" -o /tmp/chromedriver.zip

# echo "Downloading and installing chrome driver from https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
# curl -SL "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" -o /tmp/chromedriver.zip
unzip /tmp/chromedriver.zip -d /opt/render/project/.render/chrome

# Make ChromeDriver executable
chmod +x /opt/render/project/.render/chrome/chromedriver
