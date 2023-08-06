# MDNet: A Static Site Generator
MDNet is a simple static site generator that converts Markdown files into HTML files. It uses Jinja2 for templating and supports metadata in the form of YAML Front Matter

## Features
- Coverts Markdown files to HTML
- Supports YAML Front Matter for metadata
- Generates an index page with links to all posts
- Customizable with Jinja2 templates

## Installation
You can install MDNet with pip:
```
pip install mdnet
```
This will install MDNet and its dependencies, and create a command line script that you can use to run MDNet.

## Usage
After installing MDNet, you can use it like this:
```
mdnet input_dir output_dir template_path index_template_path
```
- input_dir is the directory containing the Markdown files.
- output_dir is the directory to output the HTML files to.
- template_path is the path to the HTML template for the posts.
- index_template_path is the path to the HTML template for the index page.

The templates should be Jinja2 templates. The post template will be rendered with the following variables:
- 'title': The title of the post
- 'date': the date of the post
- 'content': the content of the post

The index template will be rendered with a posts variable, which is a list of dictionaries. Each dictionary contains the 'title', 'date', and 'file' (filename) of a post.

## Example
Here's an example of how you might structure your project:
my_blog/
    mdnet/
        __init__.py
        mdnet.py
    templates/
        post.html
        index.html
    posts/
        post1.md
        post2.md
    output/

You can generate the site with this command:
```
mdnet posts output templates/post.html templates/index.html
```
This will generate HTML files in the output directory.
