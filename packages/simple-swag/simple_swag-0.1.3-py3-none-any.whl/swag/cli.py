import os
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import uuid

import fire
from multiavatar.multiavatar import multiavatar

import swag.lorem
import swag.resources
import swag.builder



def hello(name="World"):
    return f"Hello {name}!"


def start(here=""):
    root = Path(os.getcwd()) / here
    folders = ["templates", "content", "assets"]
    for folder in folders:
        if os.path.exists(root / folder):
            raise Exception("Abort! Static site directories already exist.")    
    for folder in folders:
        if not os.path.exists(root / folder):
            os.mkdir(root / folder)
    for subfolder in ["blog"]:
        if not os.path.exists(root / "content" / subfolder):
            os.mkdir(root / "content" / subfolder)
    with open(root / "templates" / "minimal.html", 'w') as f: 
        f.write(swag.resources.html_template)
    with open(root / "assets" / "styles.css", 'w') as f: 
        f.write(swag.resources.example_css)
    with open(root / "config.toml", "w") as f:
        f.write(swag.resources.example_config)
    avatar()

def avatar():
    print('generating new avatar...')
    root = swag.builder.get_project_root()
    with open(Path(root) / "assets" / "avatar.svg", "w") as f:
        f.write(multiavatar(uuid.uuid4(), None, None))

def lorem(number=10, folder='blog'):
    root = swag.builder.get_project_root()
    swag.lorem.main(root, number=number, folder=folder)

def build():
    root = swag.builder.get_project_root()
    swag.builder.main()

def serve(port = 8000, address="localhost", max_tries=3):
    root = swag.builder.get_project_root()
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(directory=root / 'build', *args, **kwargs)

    i = 0
    while i < max_tries:
        try:
            server = HTTPServer((address, port), Handler)
            print(f'\nSWAG is serving your site at https://{address}:{port}')
            server.serve_forever()
        except OSError:
            print(f'\nPort {port} is busy...')
            port += 1
            i += 1

    if i == max_tries:
        print(f'Reached attempt limit of {max_tries}, try starting with a different port')




def main():
    fire.Fire()
