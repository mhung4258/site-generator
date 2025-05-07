
from markdown_blocks import *
from page_gen import*
from static_to_public import *

md_path = './content'
tmp_path = './template.html'
dest_path = "./public"
        
def main():
    static_to_public()
    generate_pages_recursive(md_path,tmp_path,dest_path)

if __name__ == "__main__":
    main()
    

