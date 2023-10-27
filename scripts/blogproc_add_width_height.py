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

LOOKUP_STR0 = '<img src=\"{{ site.baseurl }}/assets/'
LOOKUP_STR1 = '\" '
LOOKUP_STR2 = '/>'

def run(text):
    changed = False
    
    i = text.find(LOOKUP_STR0)
    while i >= 0:
        j = text.find(LOOKUP_STR2, i)
        if j < 0:
            break
        j += len(LOOKUP_STR2)
        
        tag = text[i:j]
        parser = MyHTMLParser()
        parser.feed(tag)
        has_w = "width" in parser.attrs.keys()
        has_h = "width" in parser.attrs.keys()
        assert(has_w == has_h)
        if not has_w:
            fname_in = parser.attrs["src"].replace('{{ site.baseurl }}','..')
            assert(os.path.isfile(fname_in), f"File {fname_in} does not exist")
            dims = img_utils.img_dims(fname_in)
            parser.attrs["width"] = dims[0]
            parser.attrs["height"] = dims[1]
            
            new_tag = "<img"
            for k,v in parser.attrs.items():
                new_tag += f" {k}=\"{v}\""
            new_tag += "/>"
            print(new_tag)
            text = text[:i] + new_tag + text[j:]
            j = i + len(new_tag)
            changed = True
        
        i = text.find(LOOKUP_STR0, j)
        
    return text if changed else None
    
if __name__ == '__main__':
    blogproc.run_func_on_all_posts( run )