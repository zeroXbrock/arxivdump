import json
import os
import tarfile
from requests import get


def comb_tex_files(dir: str):
    for file in os.listdir(dir):
        if os.path.isdir(f"{dir}/{file}"):
            comb_tex_files(f"{dir}/{file}")
        elif file.endswith(".tex"):
            with open(f"{dir}/{file}", "r") as f:
                tex_files.append(f.read())


try:
    os.mkdir(f"./paper-txt")
except FileExistsError:
    pass

# read url list from json file
urls: list[str] = []
with open("url-list.json") as f:
    urls = json.load(f)

# TODO: make async

# download source from each URL and place in its own directory under paper-src
for url in urls:
    # extract paper name from url, create directory for paper
    paper_name = url.split("/")[-1]
    url_format = url.split("/")[-2]
    if url_format != "e-print":
        url = url.replace(url_format, "e-print")
    try:
        os.mkdir(f"./paper-src/{paper_name}")
    except FileExistsError:
        pass

    # download .tar.gz file from url
    src = get(url, stream=True).raw

    # unzip src .tar.gz file
    with tarfile.open(fileobj=src, mode="r|gz") as tar:
        tar.extractall(path=f"./paper-src/{paper_name}")

    # comb directory for .tex files and read each file's contents into a list
    tex_files: list[str] = []

    comb_tex_files("./paper-src")

    # concatenate contents of all .tex files into a single .txt file
    text = ""
    for file in tex_files:
        text += file + "\n"

    with open(f"./paper-txt/{paper_name}.tex", "w") as f:
        f.write(text)

print("done!")
