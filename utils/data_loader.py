import pandas as pd
from dateutil import parser
import os
from collections import defaultdict




class DataStore:
def __init__(self, csv_path='data/mock_social_trends_5000.csv'):
self.csv_path = csv_path
self._load()


def _load(self):
if not os.path.exists(self.csv_path):
raise FileNotFoundError(f"CSV not found at {self.csv_path}")
df = pd.read_csv(self.csv_path)
# Normalize column names
df.columns = [c.strip() for c in df.columns]
# Ensure timestamp parsed
df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True, errors='coerce')
# Fill NaNs in text
df['content'] = df['content'].fillna('')
df['hashtags'] = df['hashtags'].fillna('')
df['topic'] = df['topic'].fillna('Unknown')
self.df = df


# Build topics summary
self._build_topic_tables()


def _build_topic_tables(self):
topics = self.df['topic'].unique().tolist()
self.topics = {t: {'total_mentions': int((self.df['topic']==t).sum()),
'last_updated': self.df[self.df['topic']==t]['timestamp'].max()} for t in topics}
# topic mentions (for time series)
self.topic_mentions = defaultdict(list)
for _, row in self.df.iterrows():
self.topic_mentions[row['topic']].append(row['timestamp'])


def refresh(self):
self._load()