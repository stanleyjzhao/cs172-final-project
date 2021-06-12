import requests    
import re
from urllib.parse import urlparse    
import urllib.request
from bs4 import BeautifulSoup
import os
import glob

global docNum

class PyCrawler(object):     
    def __init__(self, starting_url):    
        self.starting_url = starting_url    
        self.visited = set()    

    def get_html(self, url):    
        try:    
            html = requests.get(url)    
        except Exception as e:    
            print(e)    
            return ""    
        return html.content.decode('latin-1')    

    def get_links(self, url):    
        html = self.get_html(url)    
        parsed = urlparse(url)    
        base = f"{parsed.scheme}://{parsed.netloc}"    
        links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', html)    
        for i, link in enumerate(links):    
            if not urlparse(link).netloc:    
                link_with_base = base + link    
                links[i] = link_with_base       

        return set(filter(lambda x: 'mailto' not in x, links))    

    def extract_info(self, url):    
        html = self.get_html(url)    
        meta = re.findall("<meta .*?name=[\"'](.*?)['\"].*?content=[\"'](.*?)['\"].*?>", html)    
        return dict(meta)    

    def crawl(self, url): 
        global docNum
        for link in self.get_links(url):    
            if link in self.visited:    
                continue    
            self.visited.add(link)    
            info = self.extract_info(link)    

            print(f"""Link: {link}    
            Description: {info.get('description')}    
            Keywords: {info.get('keywords')}    
            """)    
            # write html to .txt files
            html_doc = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html_doc, 'html.parser')
            # title = soup.find('title')
            file = open("htmls/" + str(docNum) + ".txt", "a")
            # file.write(link)
            # file.write("\n")
            for p in soup.find_all("p"):
                text = str(p.get_text())
                text = text.strip('\t')
                text = text.strip('\n')
                file.write(text)
            # file = open("htmls/" + str(title.string) + ".txt", "a")
            # file.write(soup.prettify())
            file.close(); 
            docNum += 1

            self.crawl(link)

    def start(self):    
        self.crawl(self.starting_url)    

if __name__ == "__main__":
    docNum = 0
    # clear out htmls folder from last run      
    files = glob.glob('htmls/*')
    for f in files:
        os.remove(f)
    seedFile = open("seedFile.txt", "r")
    lines = seedFile.readlines()
    for line in lines:
        crawler = PyCrawler(line)
        crawler.start() 