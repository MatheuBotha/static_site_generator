import shutil
import converter
import os

def copy_static_to_public():
    source_dir = "static"
    dest_dir = "public"
    try:
        shutil.rmtree(dest_dir)
        shutil.copytree(source_dir, dest_dir)
        print("Directory contents copied successfully!")
    except OSError as e:
        print(f"Error copying directory: {e}")

def write_to_file(path, content):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        print(f"File created successfully: {path}")
    except OSError as e:
        print(f"Error creating file: {e}")

def extract_title(markdown):
    first_hash_idx = markdown.find("# ")
    end_of_heading = markdown.find("\n", first_hash_idx)
    return markdown[first_hash_idx+2:end_of_heading]

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(template_path, 'r') as template_file:
        template = template_file.read()
        with open(from_path, 'r') as content_index_file:
            index_text = content_index_file.read()
            title = extract_title(index_text)
            template = template.replace("{{ Title }}", title)
            top_html_node = converter.markdown_to_html_node(index_text)
            write_to_file(dest_path, template.replace("{{ Content }}", top_html_node.to_html()))

def generate_pages_recursively(from_path, template_path, dest_path):
    for root, dirs, files in os.walk(from_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                dest_file_path = file_path.replace(from_path, dest_path)
                dest_file_path = dest_file_path.replace('.md', '.html')
                generate_page(file_path, template_path, dest_file_path)
    pass

def main():
    copy_static_to_public()
    # generate_page("content/index.md", "public/template.html", "public/index.html")
    generate_pages_recursively("content/", "public/template.html", "public/")

main()