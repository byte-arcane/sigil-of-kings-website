import os
import glob

# Run this function on all posts
# Function: return true if modified, takes all text as input and modifies it
def run_func_on_all_posts( func ):
    for post_fname in glob.glob("../_posts/*.html"):
        print("Processing file ", post_fname)
        text = open(post_fname,'rt', encoding="utf8").read()
        new_text = func(text)
        if new_text:
            open(post_fname,'wt', encoding="utf8").write(new_text)
    
if __name__ == '__main__':
    run_func_on_all_posts( lambda text_ : None )