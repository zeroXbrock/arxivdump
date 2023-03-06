import json
import os
import tarfile
from requests import get


source_dir = "./paper-src"
output_dir = "./paper-out"
url_list = "url-list.json"


def comb_tex_files(dir: str):
    for file in os.listdir(dir):
        if os.path.isdir(f"{dir}/{file}"):
            comb_tex_files(f"{dir}/{file}")
        elif file.endswith(".tex"):
            with open(f"{dir}/{file}", "r") as f:
                tex_files.append(f.read())


try:
    os.mkdir(output_dir)
except FileExistsError:
    pass

# read url list from json file
urls: list[str] = []
with open(url_list) as f:
    urls = json.load(f)

# TODO: process each paper async

# download source from each URL and place in its own directory under paper-src
for url in urls:
    # extract paper name from arxiv url, create directory for paper
    paper_name = url.split("/")[-1]
    url_format = url.split("/")[-2]
    if url_format != "e-print":
        url = url.replace(url_format, "e-print")
    try:
        os.mkdir(f"{source_dir}/{paper_name}")
    except FileExistsError:
        pass

    # download .tar.gz file from url
    src = get(url, stream=True).raw

    # unzip src .tar.gz file
    with tarfile.open(fileobj=src, mode="r|gz") as tar:
        tar.extractall(path=f"{source_dir}/{paper_name}")

    # comb directory for .tex files and read each file's contents into a list
    tex_files: list[str] = []

    comb_tex_files(f"{source_dir}")

    # concatenate contents of all .tex files into a single .txt file
    text = ""
    for file in tex_files:
        text += file + "\n"

    filenames = list(
        map(lambda ext: f"{output_dir}/{paper_name}.{ext}", ["tex", "txt"])
    )
    for filename in filenames:
        with open(filename, "w") as f:
            f.write(text)

print("done!")
