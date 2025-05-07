
from markdown_blocks import *
from page_gen import*
from static_to_public import *
import sys

md_path = './content'
tmp_path = './template.html'
dest_path = "./docs"
        
def main():

    
    args = sys.argv

    basepath = args[1] if len(args) > 1 else '/'
    static_to_public()
    generate_pages_recursive(md_path,tmp_path,dest_path,basepath)

if __name__ == "__main__":
    main()
    

