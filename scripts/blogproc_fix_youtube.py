import os
import blogproc
import img_utils
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        self.attrs = {}
        for attr in attrs:
            self.attrs[attr[0]] = attr[1]
    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

LOOKUP_STR0 = '<iframe src='
LOOKUP_STR1_0 = '/>'
LOOKUP_STR1_1 = '</iframe>'

LOOKUP_CAPTION0 = '<figcaption>'
LOOKUP_CAPTION1 = '</figcaption>'

def run(text):
    changed = False
    
    i = text.find(LOOKUP_STR0)
    while i >= 0:
        
        LOOKUP_STR1 = LOOKUP_STR1_0
        j = text.find(LOOKUP_STR1, i)
        # Try another version of the suffix string
        if j < 0:
            LOOKUP_STR1 = LOOKUP_STR1_1
            j = text.find(LOOKUP_STR1, i)
        if j < 0:
            break
        j += len(LOOKUP_STR1)
        
        tag = text[i:j]
        parser = MyHTMLParser()
        parser.feed(tag)
        if "src" in parser.attrs.keys() and "youtube" in parser.attrs['src']:
            ytcode = parser.attrs['src'].split('/')[-1]
            parser.attrs["srcdoc"] = "<style>*{padding:0;margin:0;overflow:hidden}html,body{height:100%}img,span{position:absolute;width:100%;top:0;bottom:0;margin:auto}span{height:1.5em;text-align:center;font:48px/1.5 sans-serif;color:white;text-shadow:0 0 0.5em black}</style><a href=https://www.youtube.com/embed/$YTCODE?autoplay=1><img src=https://img.youtube.com/vi/$YTCODE/hqdefault.jpg alt='video play button'><span>&#x25BA;</span></a>".replace("$YTCODE",ytcode)
            
            parser.attrs["loading"] = "lazy"
            
            title = "Showing youtube video " + ytcode
            ic = text.find(LOOKUP_CAPTION0, j)
            if ic >= 0:
                jc = text.find(LOOKUP_CAPTION1, ic)
                if jc >= 0:
                    title = text[ic+len(LOOKUP_CAPTION0):jc]
            parser.attrs["title"] = title
            
            new_tag = "<iframe"
            for k,v in parser.attrs.items():
                new_tag += f" {k}=\"{v}\""
            new_tag += "></iframe>"
            print(new_tag)
            text = text[:i] + new_tag + text[j:]
            j = i + len(new_tag)
            changed = True
        
        i = text.find(LOOKUP_STR0, j)
        
    return text if changed else None
    
if __name__ == '__main__':
    blogproc.run_func_on_all_posts( run )