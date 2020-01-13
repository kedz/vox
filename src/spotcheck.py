import argparse
from pathlib import Path
import json
import textwrap

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    args = parser.parse_args()

    with args.input.open("r") as fp:
        for i, line in enumerate(fp):
            data = json.loads(line)
            for j, s in enumerate(data["mds"]):

                for k, text in enumerate(s["summary"]):

                    print()
                    print("_" * 79)
                    print()
                    print(f"sentence page #{i}")
                    print(f"summary #{j}  ", data["date"], "\n")
                    print(textwrap.fill(f'Summary title: {s["title"]}'))
                    print(f"\nSummary Line #{k}\n")
                    print(textwrap.fill(text['text'], 
                        initial_indent='  ', subsequent_indent='  '))

                    if text["link"] in s["links"]:
                        link = s["links"][text["link"]]

                        print()
                        print(textwrap.fill(f"Article Title: {link['title']}"))
                        print(textwrap.fill(
                            f"Top Level Domain: {link['top-level-domain']}"))
                        print(textwrap.fill(
                            f"url: {link['url']}"))
                        
                        print()

                        for ll in link["text"].split("\n\n"):
                            print(textwrap.fill(ll))
                            print()
                           

                    input()





if __name__ == "__main__":
    main()
