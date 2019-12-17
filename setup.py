import os
import sys
import argparse
import subprocess
import shutil
import glob

def FormatContent(content):
    res = content.replace('/images/acac2019', 'images/acac2019')
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
for path in glob.glob(tmp + "/*.md"):
    with open(path, encoding="utf8") as f:
        content = f.read()
    formated += FormatContent(content)

with open(tmp + "/formated.md", mode='w', encoding="utf8") as f:
    f.write(formated)

os.chdir(tmp)
pandoc = ["pandoc", "formated.md", "-s", "-o", cwd + "/" + output]
subprocess.call(pandoc)
