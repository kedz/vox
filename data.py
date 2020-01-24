import json

def read_stories(f):
    days = [json.loads(l) for l in open(f, 'r').readlines()]
    stories = [s for d in days for s in d['mds']]
    #print(stories[0])
    #print(stories[1])
    #exit(0)
    return stories

def get_summaries_articles(stories):
    summaries = []
    articles = []

    for s in stories:
        for sent in s['summary']:
            url = sent['link']
            if url not in s['links']:
                continue
            summaries.append(sent['text'])
            articles.append(s['links'][url]['text'])

    return summaries, articles

if __name__ == "__main__":
    stories = read_stories('data/summaries.articles.jsonl')
    summaries, articles = get_summaries_articles(stories)
    print(summaries[0])
    print(articles[0])
