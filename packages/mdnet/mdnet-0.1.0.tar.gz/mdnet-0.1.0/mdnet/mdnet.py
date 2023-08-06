import argparse
import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

def convert_md_to_html(md):
    return markdown.markdown(md)

def get_template(template_path):
    template_dir = template_path.parent
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    return env.get_template(template_path.name)

def render_template(template_path, metadata, content):
    template = get_template(template_path)
    return template.render(title=metadata['title'], date=metadata['date'], content=content)

def render_index(template_path, posts):
    template = get_template(template_path)
    return template.render(posts=posts)

def generate_site(input_dir, output_dir, template_path, index_path):
    posts = []
    for md_file in Path(input_dir).iterdir():
        if md_file.suffix == ".md":
            post = frontmatter.load(md_file)
            html_file = output_dir / (post.metadata['title'] + ".html")
            html_file.write_text(render_template(template_path, post.metadata, convert_md_to_html(post.content)))
            posts.append({'title' : post.metadata['title'], 
                          'date' : post.metadata['date'],
                          'tldr' : post.metadata['tldr'],
                          'file' : html_file.name})
    
    (output_dir / 'index.html').write_text(render_index(index_path, posts))

def main():
    parser = argparse.ArgumentParser(description="Generate a static site from Markdown files.")
    parser.add_argument("input_dir", help="The directory containing the Markdown files.")
    parser.add_argument("output_dir", help="The directory to output the HTML files to.")
    parser.add_argument("template_path", help="The path to the HTML template.")
    parser.add_argument("index_template_path", help="The path to the index HTML template.")
    args = parser.parse_args()

    generate_site(Path(args.input_dir), Path(args.output_dir), Path(args.template_path), Path(args.index_template_path))

if __name__ == "__main__":
    main()
