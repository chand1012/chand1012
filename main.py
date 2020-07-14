import requests
from bs4 import BeautifulSoup

url = "https://chand1012.dev"

print("Getting content from " + url)
content = requests.get(url).content

print("Done. Parsing Content...")
soup = BeautifulSoup(content, features='html.parser')

main = soup.find(id='main')

links = main.findAll('a')
for link in links:
    if 'read-more' in str(link.get('class')):
        old_href = link.get('href')
        new_href = url + old_href
        link['href'] = new_href
    else:
        text = link.contents[0]
        heading = link.parent
        heading.contents[0] = text

print("Done. Reading template...")
template = ''

with open('template.md') as f:
    template = f.read()

template = template.replace('<!--content-->', str(main))

print("Writing new README...")
with open('README.md', 'w') as f:
    f.write(template)

print("Done.")