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

LOOKUP_CAPTION0 = '<figcaption>'
LOOKUP_CAPTION1 = '</figcaption>'

def run(text):
    changed = False
    
    count = 0
    
    i = text.find(LOOKUP_STR0)
    while i >= 0:
        j = text.find(LOOKUP_STR2, i)
        if j < 0:
            break
        j += len(LOOKUP_STR2)
        
        tag = text[i:j]
        parser = MyHTMLParser()
        parser.feed(tag)
        
        if "class" not in parser.attrs:
        
            src = parser.attrs["src"]
            fname_in = src.replace('{{ site.baseurl }}','..')
            assert(os.path.isfile(fname_in), f"File {fname_in} does not exist")
            dims = img_utils.img_dims(fname_in)
            parser.attrs["width"] = dims[0]
            parser.attrs["height"] = dims[1]
            parser.attrs["loading"] = "lazy" if count > 0 else "eager"
            parser.attrs["style"] = "image-resolution: from-image;"
            
            caption = "Showing image " + src
            ic = text.find(LOOKUP_CAPTION0, j)
            if ic >= 0:
                jc = text.find(LOOKUP_CAPTION1, ic)
                if jc >= 0:
                    caption = text[ic+len(LOOKUP_CAPTION0):jc]
            parser.attrs["alt"] = caption
            
            is_variant = "/variants/" in fname_in
            basename = os.path.basename(fname_in)
            stem = basename.rsplit('.',1)[0]
            
            srcset = []
            sizes = []
            all_sizes =[dims[0]] + img_utils.THUMBNAIL_SIZES
            all_sizes.sort()
            all_sizes.reverse()
            for w in all_sizes:
                if w == dims[0] or (w + img_utils.THUMBNAIL_CONV_MIN_SIZE_DIFF) < dims[0]:
                    extra = "" if w == dims[0] else f"-{w}w"
                    prefix = "" if is_variant else "variants/"
                    newbasename = f"{prefix}{stem}{extra}.webp" if "variants" not in basename else basename
                    src2 = src.replace(basename, newbasename)
                    srcset.append( f"{src2} {w}w")
            parser.attrs["srcset"] = ", ".join(srcset)
            
            # That's what linter says... 
            parser.attrs["sizes"] = "(min-width: 820px) 660px, (min-width: 520px) calc(100vw - 110px), (min-width: 460px) calc(175vw - 485px), calc(92.86vw - 89px)"
            
            # TODO: create all variants for image if they don't exist
            
            new_tag = "<img"
            for k,v in parser.attrs.items():
                new_tag += f" {k}=\"{v}\""
            new_tag += "/>"
            
            src_png = src
            if src.endswith(".webp") and "/variants/" in src:
                src = src.replace("/variants/","/").replace(".webp",".png")
            # Wrap with a href
            ahref_prefix = "<a href=\"" + src + "\" target=\"_blank\">"
            ahref_suffix = "</a>"
            while text[j:].startswith(ahref_suffix):
                j += len(ahref_suffix)
                i -= len(ahref_prefix)
            
            new_tag = ahref_prefix + new_tag + ahref_suffix
            
            text = text[:i] + new_tag + text[j:]
            j = i + len(new_tag)
            changed = True
        
        i = text.find(LOOKUP_STR0, j)
        count += 1
        
    return text if changed else None
    
if __name__ == '__main__':
    blogproc.run_func_on_all_posts( run )