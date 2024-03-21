from lxml import etree
import os


def shakespeare_lines():
    for file_name in os.listdir("shaks200"):
        if not file_name.endswith(".xml"):
            continue
        tree = etree.parse("shaks200/" + file_name)
        for line in tree.findall("//SPEECH/LINE"):
            yield (
                file_name,
                str(tree.getpath(line)),
                str(line.text),
            )
