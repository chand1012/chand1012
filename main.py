import requests
from bs4 import BeautifulSoup



url = "https://chand1012.dev"

print("Getting content from " + url)

# this fixes my encoding error
content = requests.get(url).content
content = content.replace(b'\xe2\x80\x99', b'\x27')
content = content.decode('utf-8')

print("Done. Parsing Content...")
soup = BeautifulSoup(content, features='html.parser')

posts = soup.findAll('article', attrs={"class", "post"})[:5]

for post in posts:
    links = post.findAll('a')
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

post_str = ''
for post in posts:
    post_str += f'{str(post)}\n'

template = template.replace('<!--content-->', str(post_str))

print("Writing new README...")
with open('README.md', 'w') as f:
    f.write(template)

print("Done.")