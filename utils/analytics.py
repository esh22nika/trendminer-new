import pandas as pd
import numpy as np
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import math
import re
from dateutil import parser
from functools import lru_cache
import nltk # Import nltk

# --- Setup NLTK ---
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Downloading NLTK stopwords...")
    nltk.download('stopwords')
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
     print("Downloading NLTK punkt tokenizer...")
     nltk.download('punkt')
# --- End NLTK Setup ---


from nltk.corpus import stopwords as nltk_stopwords

# More comprehensive stopwords including common English words and potentially irrelevant terms
STOPWORDS = set(nltk_stopwords.words('english')) | set([
    'a', 'an', 'the', 'and', 'or', 'for', 'to', 'in', 'on', 'with', 'at', 'by', 'is', 'are', 'was', 'were', 'of',
    'it', 'its', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
    'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'hers', 'ours', 'theirs',
    'be', 'being', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'shall', 'should', 'can', 'could',
    'may', 'might', 'must',
    'about', 'above', 'after', 'again', 'against', 'all', 'am', 'any', 'as', 'because', 'before', 'below',
    'between', 'both', 'but', 'came', 'come', 'couldnt', 'didnt', 'do', 'does', 'doing', 'dont', 'down', 'during',
    'each', 'few', 'from', 'further', 'get', 'go', 'goes', 'got', 'hadnt', 'hasnt', 'havent', 'having', 'hed',
    'hell', 'here', 'heres', 'herself', 'hes', 'himself', 'how', 'hows', 'id', 'ill', 'im', 'ive', 'if', 'into',
    'isnt', 'lets', 'like', 'make', 'many', 'more', 'most', 'much', 'no', 'nor', 'not', 'now', 'off', 'once',
    'only', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'shant', 'shed',
    'shell', 'shes', 'so', 'some', 'such', 'than', 'thats', 'the', 'their', 'theirs', 'them', 'themselves',
    'then', 'there', 'theres', 'these', 'theyd', 'theyll', 'theyre', 'theyve', 'this', 'those', 'through',
    'too', 'under', 'until', 'up', 'very', 'want', 'wasnt', 'wed', 'well', 'were', 'werent', 'weve', 'what',
    'whats', 'when', 'whens', 'where', 'wheres', 'which', 'while', 'who', 'whos', 'whom', 'why', 'whys',
    'wont', 'wouldnt', 'youd', 'youll', 'youre', 'youve', 'your', 'yours', 'yourself', 'yourselves',
    'rt', 'via', 'amp', 'new', 'one', 'post', 'see', 'also', 'just', 'like', 'know', 'get', 'think', 'thoughts' # Added common social media words
])


# --- Helper Functions ---

def format_post_for_response(row):
    """Format a DataFrame row into a post response dictionary."""
    return {
        'post_id': str(row.get('post_id', '')),
        'platform': str(row.get('platform', '')),
        'user': str(row.get('user', '')),
        'content': str(row.get('content', '')),
        'hashtags': str(row.get('hashtags', '')),
        'topic': str(row.get('topic', '')),
        'likes': int(row.get('likes', 0)),
        'shares': int(row.get('shares', 0)),
        'comments': int(row.get('comments', 0)),
        'sentiment': str(row.get('sentiment', '')),
        'timestamp': str(row.get('timestamp', '')),
        'region': str(row.get('region', ''))
    }

# --- Dashboard Analytics ---

@lru_cache()
def tracked_trends_count(datastore):
    """Counts unique topics."""
    # Ensure topics are loaded if dataframe is not empty
    if not datastore.df.empty and not hasattr(datastore, 'topics'):
         datastore._build_topic_tables()
    return len(datastore.topics)

@lru_cache()
def active_topics_count(datastore, days=14):
    """Counts topics with mentions in the last N days."""
    if days <= 0 or datastore.df.empty: return 0
     # Ensure topics are loaded
    if not hasattr(datastore, 'topics'):
         datastore._build_topic_tables()
         
    # Use UTC for cutoff calculation consistent with data
    cutoff = pd.Timestamp.utcnow() # Already UTC
    cutoff_naive = cutoff.tz_localize(None) - pd.Timedelta(days=days) # Create naive cutoff for comparison
    active = 0
    for t, meta in datastore.topics.items():
        last_updated_ts = meta.get('last_updated')
        if last_updated_ts and pd.notna(last_updated_ts):
             # Make last_updated_ts naive for comparison
             last_updated_naive = last_updated_ts.tz_convert(None) if last_updated_ts.tzinfo is not None else last_updated_ts
             if last_updated_naive >= cutoff_naive:
                active += 1
    return active


@lru_cache()
def updated_recently_count(datastore, days=7):
    """Counts topics updated within the last N days."""
    if days <= 0 or datastore.df.empty: return 0
    # Ensure topics are loaded
    if not hasattr(datastore, 'topics'):
        datastore._build_topic_tables()
        
    # Use UTC for cutoff calculation consistent with data
    cutoff = pd.Timestamp.utcnow() # Already UTC
    cutoff_naive = cutoff.tz_localize(None) - pd.Timedelta(days=days) # Create naive cutoff for comparison
    recent = 0
    for t, meta in datastore.topics.items():
        last_updated_ts = meta.get('last_updated')
        if last_updated_ts and pd.notna(last_updated_ts):
             # Make last_updated_ts naive for comparison
             last_updated_naive = last_updated_ts.tz_convert(None) if last_updated_ts.tzinfo is not None else last_updated_ts
             if last_updated_naive >= cutoff_naive:
                recent += 1
    return recent

@lru_cache()
def platform_breakdown(datastore):
    """Counts posts per platform."""
    if datastore.df.empty:
        return {}
    return datastore.df['platform'].value_counts().to_dict()

# --- Personalized Feed ---

def compute_relevance_score(datastore, interests_str, region=None):
    """Computes relevance scores for posts based on interests and region."""
    df = datastore.df.copy()

    if df.empty:
         return 0.0, pd.DataFrame(columns=list(df.columns) + ['relevance'])


    interests = [i.strip().lower() for i in interests_str.split(',') if i.strip()]

    if not interests:
        return 0.0, df.assign(relevance=0.0) # Return DataFrame with 0 relevance if no interests

    # Filter by region if specified
    if region:
        df = df[df['region'].str.lower() == region.lower()]
        if df.empty: # Check if filtering removed all data
             return 0.0, pd.DataFrame(columns=list(datastore.df.columns) + ['relevance'])


    # Calculate base relevance score (keyword matching)
    def calculate_match(row):
        score = 0
        # Combine relevant text fields for matching
        text_content = f"{row.get('topic', '')} {row.get('content', '')} {row.get('hashtags', '')}".lower()
        for interest in interests:
            # Use regex for whole word matching to avoid partial matches (e.g., 'ai' in 'rain')
            if re.search(r'\b' + re.escape(interest) + r'\b', text_content):
                score += 1
        return score

    df['match_score'] = df.apply(calculate_match, axis=1)

    # Calculate engagement weight (using the formula: likes + 2*shares + 0.5*comments)
    df['likes'] = pd.to_numeric(df['likes'], errors='coerce').fillna(0)
    df['shares'] = pd.to_numeric(df['shares'], errors='coerce').fillna(0)
    df['comments'] = pd.to_numeric(df['comments'], errors='coerce').fillna(0)
    df['engagement'] = df['likes'] + 2 * df['shares'] + 0.5 * df['comments']
    
    # Normalize engagement weight (0 to 1)
    max_engagement = df['engagement'].max()
    df['engagement_weight'] = df['engagement'] / max_engagement if max_engagement > 0 else 0

    # Calculate recency weight (using the formula: exp(-days_since_post / 7))
    now = pd.Timestamp.utcnow() # Use timezone-aware comparison
    # Ensure timestamp column is timezone-aware (UTC)
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True, errors='coerce')
    df['days_since_post'] = (now - df['timestamp']).dt.total_seconds() / (60 * 60 * 24)
    # Handle potential NaT values in timestamp before calculation
    df['days_since_post'] = df['days_since_post'].fillna(float('inf')) # Penalize missing timestamps heavily
    df['recency_weight'] = np.exp(-df['days_since_post'] / 7) # Decay factor of 7 days
    # Ensure recency_weight is 0 for future posts or NaT timestamps (already handled by fillna(inf))
    df.loc[df['days_since_post'] < 0, 'recency_weight'] = 0


    # Combine scores with specified weights: 50% match, 30% engagement, 20% recency
    df['relevance'] = (df['match_score'] * 0.5 +
                       df['engagement_weight'] * 0.3 +
                       df['recency_weight'] * 0.2)


    # Normalize final relevance score to 0-100
    max_relevance = df['relevance'].max()
    if max_relevance > 0:
        df['relevance'] = (df['relevance'] / max_relevance) * 100
    else:
        df['relevance'] = 0.0 # Avoid division by zero if all scores are 0


    # Sort by relevance
    matched_posts = df.sort_values(by='relevance', ascending=False)

    # Calculate overall relevance score (e.g., average of top 10 relevant posts' scores)
    overall_relevance = matched_posts['relevance'].head(10).mean() if not matched_posts.empty else 0.0

    return float(overall_relevance), matched_posts


# --- Trend Analysis ---

def analyze_trends(datastore, days=90):
    """Analyzes trends over the specified number of days, categorizing topics."""
    df = datastore.df.copy()

    if df.empty or days <= 0:
        return {
            "emerging_topics": [], "declining_topics": [], "peak_topics": [], "active_topics": [],
            "trend_timeline": {"categories": [], "series": {}}
        }

    cutoff_date = pd.Timestamp.utcnow().tz_localize(None) - pd.Timedelta(days=days) # Naive timestamp for filtering
    # Ensure timestamps are naive before filtering
    df['timestamp_naive'] = df['timestamp'].dt.tz_localize(None)
    df_recent = df[df['timestamp_naive'] >= cutoff_date].copy()

    if df_recent.empty:
        return {
            "emerging_topics": [], "declining_topics": [], "peak_topics": [], "active_topics": [],
            "trend_timeline": {"categories": [], "series": {}}
        }

    # Calculate daily mentions per topic
    df_recent['day'] = df_recent['timestamp'].dt.normalize() # Keep day timezone aware if possible
    topic_counts_daily = df_recent.groupby(['topic', 'day']).size().reset_index(name='mentions')

    results = {"emerging_topics": [], "declining_topics": [], "peak_topics": [], "active_topics": []}
    analyzed_topics = set()
    
    # Calculate global mention stats for percentile calculation
    all_mentions = topic_counts_daily['mentions'].values
    if len(all_mentions) == 0: # Handle case with no mentions in the period
         percentile_75 = 0
    else:
         percentile_75 = np.percentile(all_mentions, 75)


    for topic in topic_counts_daily['topic'].unique():
        topic_data = topic_counts_daily[topic_counts_daily['topic'] == topic].sort_values('day')
        mentions = topic_data['mentions'].values
        dates = topic_data['day'].values # These are normalized timestamps

        # Convert dates to naive for comparison with 'now_naive' if needed
        # dates_naive = [d.tz_localize(None) for d in dates]
        last_date_naive = dates[-1].tz_localize(None)
        now_naive = pd.Timestamp.utcnow().tz_localize(None)

        if len(mentions) < 5: # Require more data points for better trend analysis
             # Still consider it active if mentioned recently (last 14 days)
             if (now_naive - last_date_naive).days <= 14:
                 results["active_topics"].append({"topic": topic, "last_mention_count": int(mentions[-1])})
             continue


        # Growth rate calculation: compare last third to first third of the period for robustness
        third = len(mentions) // 3
        if third < 1: third = 1 # Ensure at least one element in slice
        
        avg_last = np.mean(mentions[-third:])
        avg_first = np.mean(mentions[:third])

        growth_rate = avg_last / avg_first if avg_first > 0 else (avg_last + 1) # Add 1 to avoid 0/0 or large number if start is 0
        current_mean_mentions = np.mean(mentions)

        # Heuristic classification
        is_active_recently = (now_naive - last_date_naive).days <= 14

        if growth_rate > 1.8 and avg_last > 5 and is_active_recently: # Emerging: Significant growth, recent activity, min mentions
             results["emerging_topics"].append({"topic": topic, "growth_rate": round(growth_rate, 2), "avg_mentions": round(current_mean_mentions, 1)})
             analyzed_topics.add(topic)
        elif growth_rate < 0.6 and avg_first > 5: # Declining: Significant drop from previous activity
             results["declining_topics"].append({"topic": topic, "decline_rate": round(growth_rate, 2), "avg_mentions": round(current_mean_mentions, 1)})
             analyzed_topics.add(topic)
        elif 0.8 <= growth_rate <= 1.2 and current_mean_mentions > percentile_75 and is_active_recently: # Peak: Stable, high mentions relative to others, active recently
             results["peak_topics"].append({"topic": topic, "avg_mentions": round(current_mean_mentions, 1)})
             analyzed_topics.add(topic)

        # Active topics check (mentioned in last 14 days) - add if not already categorized
        if topic not in analyzed_topics and is_active_recently:
             results["active_topics"].append({"topic": topic, "last_mention_count": int(mentions[-1])})
             analyzed_topics.add(topic)

    # Build Trend Timeline for specific categories
    # Using the categories from the prompt
    categories = ["AI & Large Language Models", "Electric Vehicles", "Entertainment & Music", "Cricket"] # Corrected "Sports" to "Cricket" based on data
    timeline_series = defaultdict(list)
    df_timeline = df_recent[df_recent['topic'].isin(categories)]
    
    # Ensure 'day' column exists and is timezone-aware or naive consistently
    if not df_timeline.empty:
         # Use dt accessor for timezone-aware or naive conversion
         df_timeline['day_str'] = df_timeline['day'].dt.strftime('%Y-%m-%d')
         timeline_counts = df_timeline.groupby(['topic', 'day_str']).size().reset_index(name='count')

         for topic in categories:
             topic_data = timeline_counts[timeline_counts['topic'] == topic].sort_values('day_str')
             for _, row in topic_data.iterrows():
                 timeline_series[topic].append({"date": row['day_str'], "count": int(row['count'])})
    else: # Handle case where none of the target categories are in recent data
         for topic in categories:
             timeline_series[topic] = []


    results["trend_timeline"] = {
        "categories": categories,
        "series": dict(timeline_series)
    }

    # Sort results for consistency (optional)
    # (Sorting logic from previous step is retained here)
    for key in ["emerging_topics", "declining_topics", "peak_topics", "active_topics"]:
        if results[key] and isinstance(results[key][0], dict):
             # Define sort key based on available metric
             if 'growth_rate' in results[key][0]: sort_key = 'growth_rate'; reverse = True
             elif 'decline_rate' in results[key][0]: sort_key = 'decline_rate'; reverse = False
             elif 'avg_mentions' in results[key][0]: sort_key = 'avg_mentions'; reverse = True
             elif 'last_mention_count' in results[key][0]: sort_key = 'last_mention_count'; reverse = True
             else: sort_key = 'topic'; reverse=False # Fallback sort key
             try:
                 # Use .get with a default for safe sorting
                 results[key] = sorted(results[key], key=lambda x: x.get(sort_key, 0) if isinstance(x.get(sort_key), (int, float)) else 0, reverse=reverse)
             except TypeError: # Handle potential comparison issues if metrics aren't numeric
                  results[key] = sorted(results[key], key=lambda x: str(x.get(sort_key, '')))

    return results


def platform_comparison(datastore, topic, start=None, end=None):
    """Compares topic performance across platforms over time."""
    df = datastore.df.copy()

    if df.empty:
        return {}
        
    if topic:
        # Case-insensitive topic filtering
        df = df[df['topic'].str.lower() == topic.lower()]

    # Convert start/end strings to datetime if provided (make them timezone-aware UTC)
    start_date = pd.to_datetime(start, utc=True, errors='coerce') if start else None
    end_date = pd.to_datetime(end, utc=True, errors='coerce') if end else None

    # Filter by date range (already timezone-aware)
    if start_date:
        df = df[df['timestamp'] >= start_date]
    if end_date:
        # Add one day to end_date to include the full end day
        end_date_inclusive = end_date + pd.Timedelta(days=1)
        df = df[df['timestamp'] < end_date_inclusive]

    if df.empty:
        return {}

    df['day'] = df['timestamp'].dt.normalize() # Normalize to day (keeps timezone)

    # Calculate engagement sum (using correct formula from prompt)
    df['likes'] = pd.to_numeric(df['likes'], errors='coerce').fillna(0)
    df['shares'] = pd.to_numeric(df['shares'], errors='coerce').fillna(0)
    df['comments'] = pd.to_numeric(df['comments'], errors='coerce').fillna(0)
    # Ensure correct formula: likes + 2*shares + 0.5*comments (This differs from platform_comparison prompt, using this one as requested elsewhere)
    # The prompt for platform_comparison specifically asked for engagement_sum and avg_sentiment. Let's stick to sum = L+S+C for this endpoint.
    df['engagement_sum'] = df['likes'] + df['shares'] + df['comments']


    # Map sentiment to numerical values for averaging
    sentiment_map = {'Positive': 1, 'Neutral': 0, 'Negative': -1}
    df['sentiment_score'] = df['sentiment'].map(sentiment_map).fillna(0) # Fill NaN sentiments with Neutral (0)


    # Group by platform and day
    platform_daily = df.groupby(['platform', 'day']).agg(
        total_mentions=('post_id', 'count'),
        engagement_sum=('engagement_sum', 'sum'),
        sentiment_score_sum=('sentiment_score', 'sum')
    ).reset_index()

    # Calculate average sentiment score
    # Ensure division by zero doesn't occur if total_mentions is 0 (though groupby should handle this)
    platform_daily['avg_sentiment_score'] = platform_daily.apply(
        lambda row: row['sentiment_score_sum'] / row['total_mentions'] if row['total_mentions'] > 0 else 0,
        axis=1
    )
    # Returning the numeric score rounded to 2 decimal places
    platform_daily['avg_sentiment'] = platform_daily['avg_sentiment_score'].round(2)

    # Format for response, ensuring dates are strings
    results = defaultdict(list)
    for _, row in platform_daily.iterrows():
        results[row['platform']].append({
            'date': row['day'].strftime('%Y-%m-%d'),
            'mentions': int(row['total_mentions']),
            'engagement_sum': int(row['engagement_sum']), # Ensure integer
            'avg_sentiment': float(row['avg_sentiment']) # Ensure float
        })
        
    # Sort the time series data within each platform
    for platform in results:
        results[platform] = sorted(results[platform], key=lambda x: x['date'])


    return dict(results) # Convert back to dict for JSON


# --- Pattern Mining ---

def extract_phrases(text, ngram_range=(2, 3)):
    """Extracts n-gram phrases from text, removing stopwords."""
    if not isinstance(text, str):
        return set()
    words = [w for w in re.findall(r"\b\w+\b", text.lower()) if w not in STOPWORDS and len(w) > 1] # Ensure words have length > 1
    phrases = set()
    for n in range(ngram_range[0], ngram_range[1] + 1):
        for i in range(len(words) - n + 1):
            p = ' '.join(words[i:i + n])
            # Basic check to avoid overly generic phrases if needed (optional)
            # Example: if len(p.split()) > 1 and not all(word in SOME_GENERIC_LIST for word in p.split()):
            if len(p.strip()) > 3: # Keep simple length check
                phrases.add(p)
    # Basic named entity heuristic (optional, can be improved with proper NER)
    # capitalized_words = re.findall(r"\b[A-Z][a-z]+\b(?:\s+[A-Z][a-z]+)*", text)
    # for cw in capitalized_words:
    #     phrases.add(cw.lower())
    return phrases

@lru_cache()
def pattern_rules(datastore, limit=50, min_cooccurrence=3):
    """Identifies topic-phrase co-occurrence rules."""
    df = datastore.df.copy()
    if df.empty:
        return []

    # Candidate phrase extraction
    phrase_counts = Counter()
    topic_phrase_map = defaultdict(Counter)
    post_phrases = {} # Map post_id to its set of phrases

    # Ensure text columns are strings before processing
    df['content'] = df['content'].astype(str)
    df['hashtags'] = df['hashtags'].astype(str)
    df['topic'] = df['topic'].astype(str)


    for _, row in df.iterrows():
        # Combine content and hashtags for phrase extraction
        text = row['content'] + ' ' + row['hashtags']
        phrases = extract_phrases(text)
        post_id = row['post_id']
        post_phrases[post_id] = phrases
        topic = row['topic']
        for p in phrases:
            phrase_counts[p] += 1
            topic_phrase_map[topic][p] += 1

    # Build co-occurrence of topic-phrase pairs
    rules = []
    for topic, phrase_counter in topic_phrase_map.items():
        # Iterate through phrases for the current topic, ordered by frequency
        for phrase, count in phrase_counter.most_common(): # Get all phrases, sort later
            if count < min_cooccurrence:
                continue

            # Find example posts (limit to 3 examples)
            examples = []
            # Iterate through post_ids associated with the current topic first for efficiency
            topic_post_ids = df[df['topic'] == topic]['post_id'].tolist()
            
            posts_checked = 0
            # Prioritize posts belonging to the rule's topic
            for post_id in topic_post_ids:
                 if post_id in post_phrases and phrase in post_phrases[post_id]:
                     row_data = df[df['post_id'] == post_id].iloc[0] # Get the first row matching post_id
                     examples.append({
                         'post_id': int(row_data['post_id']),
                         'content': row_data['content'][:200] + ('...' if len(row_data['content']) > 200 else '') # Truncate content
                     })
                     if len(examples) >= 3:
                         break
                 posts_checked += 1
                 # Optional: Limit search space for performance if dataset is very large
                 # if posts_checked > 1000: break 
            
            # If fewer than 3 examples found in topic posts, search remaining posts (optional)
            # This might be slow on large datasets and less relevant to the "topic-phrase" rule concept
            # if len(examples) < 3:
            #    # ... logic to search other posts ...


            # Format the rule string as specified in the prompt
            rule_str = f"{topic} often appears with phrase '{phrase}'"

            rules.append({
                'rule': rule_str,
                'cooccurrence_count': int(count),
                'examples': examples
            })

    # Sort rules by co-occurrence count descending and take the limit
    rules.sort(key=lambda x: x['cooccurrence_count'], reverse=True)

    return rules[:limit]

# --- Topic Explorer ---

def topic_time_series(datastore, topic):
    """Generates a daily time series of mention counts for a specific topic."""
    df = datastore.df.copy()
    if df.empty or topic not in datastore.topics:
        return []

    topic_df = df[df['topic'] == topic].copy()
    if topic_df.empty:
         return []

    # Ensure timestamp is datetime and normalize to day
    topic_df['day'] = pd.to_datetime(topic_df['timestamp']).dt.normalize()
    
    # Count mentions per day
    time_series = topic_df.groupby('day').size().reset_index(name='count')
    
    # Format for JSON response
    series_data = []
    for _, row in time_series.iterrows():
        series_data.append({
            'date': row['day'].strftime('%Y-%m-%d'),
            'count': int(row['count'])
        })
        
    # Sort by date
    series_data.sort(key=lambda x: x['date'])

    return series_data