import os
import blogproc
import img_utils

LOOKUP_STR0 = '<img src=\"{{ site.baseurl }}/assets/'
LOOKUP_STR1 = '\" '

def replace_with_variant(text, thumb):
    base = os.path.dirname(text)
    stem = os.path.basename(text).rsplit('.',1)[0]
    thumb_text = f'-{thumb}w' if thumb else ''
    return f"{base}/variants/{stem}{thumb_text}.webp"

def run(text):
    changed = False
    # before end of metadata, if "image: " is found, replace .png with .webp
    i_metadata_end = text.index('---',1)
    if ('image: ' in text[:i_metadata_end]) and False:
        i0 = text.index('image: ')
        i0 += len('image: ')
        i1 = text.index('\n', i0)
        path = text[i0:i1]
        print(path)
        if path.endswith('.png'):
            path_dir = os.path.dirname(path)
            path_stem = os.path.basename(path)[:-4]
            text[i0:i1] = f"{path_dir}/variants/{path_stem}.webp"
            changed = True
    
    # TODO: locate all <img tags and augment
    i = text.find(LOOKUP_STR0)
    while i >= 0:
        i +=len(LOOKUP_STR0)
        j = text.find(LOOKUP_STR1, i)
        if j < 0:
            break
        
        path = text[i:j]
        if ".png" in path:
            srcset = "\" srcset=\""
            any_used = False
            for THUMBNAIL_SIZE in img_utils.THUMBNAIL_SIZES:
                if os.path.isfile('../assets/'+replace_with_variant(path, THUMBNAIL_SIZE)):
                    srcset += '{{ site.baseurl }}/assets/' + replace_with_variant(path, THUMBNAIL_SIZE) + f" {THUMBNAIL_SIZE}w, "
                    any_used = True
            srcset = srcset[:-2] if any_used else ""
            text = text[:i] + replace_with_variant(path, None) + srcset + text[j:]
            changed = True
        
        i = text.find(LOOKUP_STR0, j)
        
    return text if changed else None
    
if __name__ == '__main__':
    blogproc.run_func_on_all_posts( run )