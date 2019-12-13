import argparse
from pathlib import Path
import json

test_url = "https://www.vox.com/vox-sentences/2017/6/30/15906502/vox-sentences-trumps-voting-commission-wont-honor-request-state-data"

test_url = "https://www.vox.com/vox-sentences/2019/10/11/20910428/giuliani-trump-impeachment-fraud-guarantee-nobel-prize"

test_url = "https://www.vox.com/vox-sentences/2018/10/30/18045140/vox-sentences-trump-birthright-citizenship"

test_url = "https://www.vox.com/vox-sentences/2018/8/21/17766286/vox-sentences-cohen-manafort-guilty"

import requests
import re


def craw_sentence_url(sentence_url):

    raw_html = requests.get(sentence_url).content.decode('utf8')

    stories = []
    for header, lines in re.findall(r'<h3\s*(?:id|class)="\w+">(?:<strong>)?(\w.+?)(?:</strong>)?</h3>.*?<ul.*?>(.+?)</ul>', raw_html, flags=re.DOTALL):

        if header.strip() in ["Watch this:", "Verbatim"]:
            continue
        if header.startswith("Watch this"):
            continue
        print(header)
        print()
        summary_lines = []
        for line in re.findall(r"<li.*?>(.*?)</li>", lines, flags=re.DOTALL):
            text = re.sub(r'<a.*', "", line).strip()
            if text[-1:] == "[":
                text = text[:-1].strip()
 
            m = re.search(r'<a href="(.*?)">(.*?)</a>', line)
            if m is not None:
                url, attribution = m.groups()
                attribution = attribution.strip()
                if attribution[0] == "[":
                    attribution = attribution[1:]
                if attribution[-1] == "]":
                    attribution = attribution[:-1]
               
                summary_lines.append(
                    {"text": text, "url": url, "attribution": attribution})
            else:
                url = None
                attribution = None
            import textwrap

            print(textwrap.fill(text))
            print(attribution)
            print(url)
            
            print()
        stories.append({"header": header, "summary": summary_lines}) 
        print()
    return {"stories": stories, "url": sentence_url}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    urls = args.urls.read_text().strip().split("\n")
    
    args.output.parent.mkdir(exist_ok=True, parents=True)
    with args.output.open("w") as fp:
        for i, url in enumerate(urls):
            if "2015" in url:
                continue
            if "2014" in url:
                continue
            print(url)

            print(i, len(urls))
            data = craw_sentence_url(url)
            from pprint import pprint
            pprint(data)
            print(json.dumps(data), file=fp)
            print(i, len(urls))
            
            

if __name__ == "__main__":
    main()
