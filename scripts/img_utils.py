import os
import tempfile
import subprocess
import glob
from PIL import Image

THUMBNAIL_SIZES = [320, 640, 960]
THUMBNAIL_CONV_MIN_SIZE_DIFF = 100

def img_dims( fname_in ):
    return Image.open(fname_in).size

def img_resize( fname_in, fname_out, new_width ):
    
    im_in = Image.open(fname_in)
    if im_in.size[0] > (new_width+THUMBNAIL_CONV_MIN_SIZE_DIFF):
        print("Resizing image ",fname_in)
        ar = new_width / im_in.size[0]
        new_height = int(round(im_in.size[1] * ar))
        im_out = im_in.resize((new_width, new_height), resample=Image.LANCZOS)
        im_out.save(fname_out)
        return True
    else:
        return False

def img_to_webp( fname_in, fname_out ):
    cwebp = "c:/Tools/libwebp-1.3.1-windows-x64/bin/cwebp.exe"
    if not os.path.isfile(fname_out):
        print("Converting image to webp: ",fname_in)
        subprocess.run(f"{cwebp} -near_lossless 0 {fname_in} -o {fname_out}")
    
# Convert an image to sized variant web images
def img_to_sized_variants( fname_in ):
    # <img src="flower-320w.jpg" srcset="flower-320w.jpg 320w, flower-640w.jpg 640w, flower-960w.jpg 960w">
    
    variants_dir = os.path.dirname(fname_in) + "/variants"
    if not os.path.isdir(variants_dir):
        os.makedirs(variants_dir)
    
    fnames = []
    stem = os.path.basename(fname_in).rsplit('.',1)[0]
    fname_out = variants_dir + "/" + stem + ".webp"
    img_to_webp(fname_in, fname_out)
    for THUMBNAIL_SIZE in THUMBNAIL_SIZES:
        fname_out = variants_dir + "/" + stem + f"-{THUMBNAIL_SIZE}w.webp"
        if not os.path.isfile(fname_out):
            fname_resized = f"{tempfile.gettempdir()}/{stem}-{THUMBNAIL_SIZE}.png"
            did_resize = img_resize(fname_in, fname_resized, THUMBNAIL_SIZE)
            if did_resize:
                img_to_webp(fname_resized, fname_out)
                fnames.append(fname_out)
                
def img_optipng(fname_in ):
    cmd = f"C:\\Tools\\Portable\\optipng.exe -o7 -fix {fname_in}"
    print(cmd)
    subprocess.run(cmd)
        
if __name__ == '__main__':
    
    #img_to_sized_variants('C:/Users/esrev/Dropbox/sok_music/lair_dragon.png')
    root = '../assets'
    for fname in glob.iglob(f'{root}/**/*.png', recursive=True):
        img_optipng(fname)
    