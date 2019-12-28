import os
import sys
import argparse
import subprocess
import shutil
import glob
import re

def FormatQuote(content, prefix):
    res = re.sub(r"\[\^(.+?)\]", r"[^" + str(prefix) + r"-\1]", content, flags=re.MULTILINE)
    res = re.sub(r"^(\[\^.+?\]:.*)$", "\n" + r"\1" + "\n", res, flags=re.MULTILINE)
    return res

def FormatContent(content, prefix):
    res = content.replace('/images/acac2019', 'images/acac2019')
    res = re.sub(r"([^!])\[(.*)\]\((.*)\)", r"\1\2(\3)", res, flags=re.MULTILINE)
    res = re.sub(r"^#", r"##", res, flags=re.MULTILINE)
    res = re.sub(r"  " + "\n" + r"(?!\[\^\d+\])", r"", res, flags=re.MULTILINE|re.DOTALL)
    res = FormatQuote(res, prefix)
    res = re.sub(r"^\+\+\+.*title\s*=\s*\"(.*?)\".*authors\s*=\s\[\"(.*?)\"\].*\+\+\+",
     r"# \1" + "\n" + r"###### \2", res, flags=re.DOTALL)
    res += "\n"
    res += "\n"
    return res

parser = argparse.ArgumentParser(description='Set up ACAC icml')
parser.add_argument('output', metavar='OUTPUT', type=str, help='output path')
parser.add_argument('--md', help='input markdown directory path')
parser.add_argument('--image', help='input image directory path')

output = "acac2019.icml"
md = ""
image = ""
tmp = "tmp"

args = parser.parse_args()
if args.output != "":
    output = args.output

if not os.path.exists(args.md):
    print("not exsist markdown directory")
    exit()
md = args.md

if not os.path.exists(args.image):
    print("not exsist image directory")
    exit()
image = args.image

if os.path.exists(os.path.dirname(__file__) + "/" + tmp):
    shutil.rmtree(os.path.dirname(__file__) + "/" + tmp)

shutil.copytree(md, os.path.dirname(__file__) + "/" + tmp)
shutil.copytree(image, os.path.dirname(__file__) + "/" + tmp + "/images")

cwd = os.getcwd()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

formated = ""
i = 0
for path in glob.glob(tmp + "/*.md"):
    if path.count("_index") > 0:
        continue
    with open(path, encoding="utf8") as f:
        content = f.read()
    formated += FormatContent(content, i)
    i += 1

with open(tmp + "/formated.md", mode='w', encoding="utf8") as f:
    f.write(formated)

os.chdir(tmp)
pandoc = ["pandoc", "formated.md", "-s", "-o", cwd + "/" + output]
subprocess.call(pandoc)
