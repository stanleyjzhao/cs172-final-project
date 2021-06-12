import requests   
import threading
import re
from urllib.parse import urlparse    
import urllib.robotparser
import urllib.request
from bs4 import BeautifulSoup
import os
import glob

global docNum

class PyCrawler(object):     
    def __init__(self, starting_url):    
        self.starting_url = starting_url  
        rp.set_url(starting_url.rstrip() + "robots.txt")
        rp.read()

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
            if link in visited or not rp.can_fetch("*", link):
                continue    
            visited.add(link)    
            info = self.extract_info(link)    

            print(f"""Link: {link}    
            Description: {info.get('description')}    
            Keywords: {info.get('keywords')}    
            """)    
            # write html to .txt files
            html_doc = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html_doc, 'html.parser')
            file = open("htmls/" + str(docNum) + ".txt", "a")
            file.write(link)
            file.write("\n")
            
            for p in soup.find_all("p"):
                text = str(p.get_text())
                text = text.strip('\t')
                text = text.strip('\n')
                file.write(text)
            # file = open("htmls/" + str(title.string) + ".txt", "a")
            # file.write(soup.prettify())
                file.write(p.get_text())

            file.close(); 
            docNum += 1

            self.crawl(link)

    def start(self):    
        self.crawl(self.starting_url)    

if __name__ == "__main__":
    rp = urllib.robotparser.RobotFileParser()
    visited = set()
    docNum = 0
    # clear out htmls folder from last run      
    files = glob.glob('htmls/*')
    for f in files:
        os.remove(f)
    # crawl every link in seedFile.txt
    seedFile = open("seedFile.txt", "r")
    lines = seedFile.readlines()


    # crawl using 3 threads
    i = 0
    while i < len(lines):
        thread1 = threading.Thread(target=(PyCrawler(lines[i]).start))
        if (lines[i + 1]):
            thread2 = threading.Thread(target=(PyCrawler(lines[i + 1]).start))
        else:
            thread2 = threading.Thread(target=())
        if (lines[i + 2]):
            thread3 = threading.Thread(target=(PyCrawler(lines[i + 2]).start))
        else:
            thread3 = threading.Thread(target=())
        
        thread1.start()
        thread2.start()
        thread3.start()
        thread1.join()  
        thread2.join()
        thread3.join()
        i += 3