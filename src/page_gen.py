from markdown_blocks import *
import os

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from [{from_path}] to [{dest_path}] using [{template_path}]")

    with open(from_path) as md_file, open(template_path) as tmp_file:
        md = md_file.read()
        template = tmp_file.read()

    html_string = markdown_to_html_node(md).to_html()
    title = extract_title(md)

    #replace title and content
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')


    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as file:
        file.write(template)
    print("File Generated")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):    
    for file in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(from_path):
            dest_path = os.path.splitext(dest_path)[0] + '.html'
            generate_page(from_path, template_path,dest_path,basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
    