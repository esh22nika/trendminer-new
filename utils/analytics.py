import pandas as pd
import numpy as np
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import math
import re


STOPWORDS = set([w.strip() for w in "a,an,the,and,or,for,to,in,on,with,at,by,is,are,was,were,of".split(',')])




def tracked_trends_count(datastore):
return len(datastore.topics)




def active_topics_count(datastore, days=14):
cutoff = pd.Timestamp.utcnow() - pd.Timedelta(days=days)
active = [t for t,meta in datastore.topics.items() if meta['last_updated'] is not pd.NaT and pd.Timestamp(meta['last_updated']) >= cutoff]
return len(active)




def updated_recently_count(datastore, days=7):
cutoff = pd.Timestamp.utcnow() - pd.Timedelta(days=days)
recent = [t for t,meta in datastore.topics.items() if meta['last_updated'] is not pd.NaT and pd.Timestamp(meta['last_updated']) >= cutoff]
return len(recent)




def platform_breakdown(datastore):
return datastore.df['platform'].value_counts().to_dict()

# Relevance scoring utilities


def extract_phrases(text, ngram_range=(2,3)):
words = [w for w in re.findall(r"\w+", text.lower()) if w not in STOPWORDS]
phrases = set()
for n in range(ngram_range[0], ngram_range[1]+1):
for i in range(len(words)-n+1):
p = ' '.join(words[i:i+n])
if len(p.strip())>3:
phrases.add(p)
# also detect named entity like consecutive capitalized words using a simple heuristic
# (caller should also pass original text for capitalization detection)
return phrases




def pattern_rules(datastore, limit=50, min_cooccurrence=3):
df = datastore.df.copy()
# candidate phrase extraction
phrase_counts = Counter()
topic_phrase_map = defaultdict(Counter)
post_phrases = {}
for _, row in df.iterrows():
text = (row['content'] or '') + ' ' + (row['hashtags'] or '')
phrases = extract_phrases(text)
post_phrases[row['post_id']] = phrases
for p in phrases:
phrase_counts[p]+=1
topic_phrase_map[row['topic']][p]+=1


# build co-occurrence of topic-phrase pairs
rules = []
for topic, pc in topic_phrase_map.items():
for phrase, cnt in pc.most_common(200):
if cnt<min_cooccurrence:
continue
# find example posts
examples = []
for pid, phs in post_phrases.items():
if phrase in phs:
row = df[df['post_id']==pid].to_dict('records')
if row:
examples.append({'post_id': pid, 'content': row[0]['content']})
if len(examples)>=3:
break
rules.append({'rule': f"{topic} often appears with phrase '{phrase}'", 'cooccurrence_count': int(cnt), 'examples': examples})
if len(rules)>=limit:
break
return rules