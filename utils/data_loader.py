import pandas as pd
from dateutil import parser
import os
from collections import defaultdict
from functools import lru_cache
import schedule
import time
import threading

class DataStore:
    def __init__(self, csv_path='data/mock_social_trends_5000.csv'):
        self.csv_path = csv_path
        self._load()
        self._schedule_refresh()

    @lru_cache(maxsize=None)
    def _load(self):
        """Loads and preprocesses the CSV data."""
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"CSV not found at {self.csv_path}")

        df = pd.read_csv(self.csv_path)
        # Normalize column names (strip whitespace)
        df.columns = [c.strip() for c in df.columns]
        # Ensure timestamp is parsed as UTC datetime objects
        df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True, errors='coerce')
        # Fill missing text values
        df['content'] = df['content'].fillna('')
        df['hashtags'] = df['hashtags'].fillna('')
        df['topic'] = df['topic'].fillna('Unknown')
        self.df = df

        # Build topics summary
        self._build_topic_tables()

    def _build_topic_tables(self):
        """Builds summary tables for topics."""
        if self.df.empty:
            self.topics = {}
            self.topic_mentions = defaultdict(list)
            return

        topics = self.df['topic'].unique().tolist()
        self.topics = {
            t: {
                'total_mentions': int((self.df['topic'] == t).sum()),
                'last_updated': self.df[self.df['topic'] == t]['timestamp'].max()
            } for t in topics
        }
        # Topic mentions for time series analysis
        self.topic_mentions = defaultdict(list)
        for _, row in self.df.iterrows():
            self.topic_mentions[row['topic']].append(row['timestamp'])

    def refresh(self):
        """Reloads the data from the CSV and clears caches."""
        print("Refreshing data store...")
        self._load.cache_clear()  # Clear the cache to force a reload
        self._load()
        print("Data store refreshed.")
        
    def _schedule_refresh(self):
        """Schedules the data refresh to run periodically."""
        schedule.every(24).hours.do(self.refresh)
        
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(1)

        # Run the scheduler in a separate thread
        thread = threading.Thread(target=run_scheduler)
        thread.daemon = True
        thread.start()