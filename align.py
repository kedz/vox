from rouge_score.rouge_scorer import RougeScorer
import numpy as np

from data import read_stories, get_summaries_articles

def align_simple(summaries, articles, metric='rouge2'):
    scorer = RougeScorer([metric], use_stemmer=False)
    aix = []
    asn = []
    
    for s, a in zip(summaries, articles):
        #print(a)
        #s = s.lower()
        sentences = [p.strip() for p in a.split('\n') if p != '']
        #sentences = [sent.lower() for p in paragraphs for sent in p.split('. ')]
        if len(sentences) == 0:
            continue
        scores = [scorer.score(s, sent)[metric].fmeasure for sent in sentences]
        #print(scores[0])
        #exit(0)
        i = np.argmax(scores)
        print(s)
        print(sentences[i])
        print()
        aix.append(i)
        asn.append(sentences[i])

    return aix, asn

if __name__ == "__main__":
    stories = read_stories('data/summaries.articles.jsonl')
    summaries, articles = get_summaries_articles(stories)
    #print(summaries[0])
    #print(articles[0])
    indices, sentences = align_simple(summaries, articles)
