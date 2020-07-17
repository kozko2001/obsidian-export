import argparse
import re
import os

METADATA_RE = re.compile("""-\W+(reference|metadata)(.*?)\n(?P<metadata>.*?)\n-""", re.DOTALL)
ATTRIBUTES_RE = re.compile("""\W+([A-z]+?)::\W+(.*)\W*""")
REMOVE_FIRST_LEVEL_RE = re.compile("""^-\s+""")
REPLACE_TWO_SPACES= re.compile("""^\s{4}""")

def read(args):
    markdown = args.infile.read()
    args.infile.close()

    return markdown

def getMetadata(markdown):
    metadata = re.match(METADATA_RE, markdown)

    return metadata.groupdict()['metadata'] if metadata else None

def getAttributes(metadata):
    attr = {}

    for line in metadata.split("\n"):
        attributes = re.match(ATTRIBUTES_RE, line)
        if attributes:
            name, value = attributes.groups()
            attr[name] = value

    return attr

def getBlogAttributes(metadata):
    attributes = getAttributes(metadata)

    blog = attributes["blog"]
    date = attributes["date"] if "date" in attributes else None

    return blog, date

def removeOneLevel(markdown):
    lines = markdown.split("\n")
    lines = [REMOVE_FIRST_LEVEL_RE.sub("\n\n", line) for line in lines]
    lines = [REPLACE_TWO_SPACES.sub("  ", line) for line in lines]

    return "\n".join(lines)


def getOutputFile(args):
    infile = args.infile.name
    outfolder = args.outfolder

    return os.path.join(outfolder, os.path.basename(infile))

def main():
    parser = argparse.ArgumentParser(description="from roam to hugo")
    parser.add_argument("-i", dest="infile", required=True, 
                        type=argparse.FileType('r', encoding='UTF-8'))
    parser.add_argument("-o", dest="outfolder", required=True, type=str)

    args = parser.parse_args()

    ## Read Markdown
    markdown = read(args)

    metadata = getMetadata(markdown)
    blog, date = getBlogAttributes(metadata)


    markdown_no_metadata = "-" + METADATA_RE.sub("", markdown)
    markdown_no_metadata = removeOneLevel(markdown_no_metadata)

    
    markdown = f"""
---
title: {blog}
date: {date}
---
""" + markdown_no_metadata


    with open(getOutputFile(args), "w") as f:
        f.write(markdown)

if __name__ == "__main__":
    main()
