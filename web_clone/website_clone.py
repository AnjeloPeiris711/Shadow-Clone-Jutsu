# Shadow-Clone-Jutsu: Webiste Clone v0.0

import urllib.request

def clone(url):
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf-8')  # Decode the response using 'utf-8'
    return html

user_input = input("Enter the link of the website you want to clone: ")

with open("clone.html", 'w', encoding='utf-8') as output:  # Specify 'utf-8' encoding when opening the file
    output.write(clone(user_input))

print("Website cloned successfully, check clone.html :)")
