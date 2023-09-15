# Shadow-Clone-Jutsu: Webiste Clone v0.0

import urllib.request
from bs4 import BeautifulSoup
import os
import requests
from urllib.parse import urljoin

class WebPageCloner:
    def __init__(self, url, output_folder):
        self.url = url
        self.output_folder = output_folder

    def clone(self):
        # Create the output folder if it doesn't exist
        os.makedirs(self.output_folder, exist_ok=True)

        # Download the main HTML content
        html = self.download(self.url)

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Find and download CSS files
        css_links = soup.find_all('link', rel='stylesheet')
        for link in css_links:
            css_url = link.get('href')
            if css_url:
                full_css_url = urljoin(self.url, css_url)  # Construct the complete CSS URL
                self.download(full_css_url)

        # Save the main HTML content
        with open(os.path.join(self.output_folder, 'index.html'), 'w', encoding='utf-8') as html_file:
            html_file.write(str(soup))

        print("Website cloned successfully. Check the output folder.")

    def download(self, url):
        response = requests.get(url)
        content = response.text
        return content

if __name__ == "__main__":
    user_input = input("Enter the link of the website you want to clone: ")
    output_folder = input("Enter the name of the output folder: ")

    cloner = WebPageCloner(user_input, output_folder)
    cloner.clone()
