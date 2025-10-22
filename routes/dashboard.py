from flask import Blueprint, current_app, jsonify, request
dashboard_bp = Blueprint('dashboard', __name__)




@dashboard_bp.route('/summary')
def summary():
ds = current_app.config['DATASTORE']
res = {
'tracked_trends_count': tracked_trends_count(ds),
'active_topics_count': active_topics_count(ds, days=14),
'updated_recently_count': updated_recently_count(ds, days=7),
'platform_breakdown': platform_breakdown(ds),
'top_topics': sorted([{'topic':k,'mentions':v['total_mentions'],'last_updated': str(v['last_updated'])} for k,v in ds.topics.items()], key=lambda x: x['mentions'], reverse=True)[:10]
}
return jsonify(res)




@dashboard_bp.route('/for-you')
def for_you():
ds = current_app.config['DATASTORE']
interests = request.args.get('interests', '')
region = request.args.get('region')
limit = int(request.args.get('limit', 20))
relevance_score, matched_posts = compute_relevance_score(ds, interests, region)
# simplify posts for response
posts = []
for _, row in matched_posts.head(limit).iterrows():
posts.append({
'post_id': int(row['post_id']),
'platform': row['platform'],
'user': row['user'],
'content': row['content'],
'topic': row['topic'],
'likes': int(row['likes'] or 0),
'shares': int(row['shares'] or 0),
'comments': int(row['comments'] or 0),
'timestamp': str(row['timestamp']),
'relevance_score': float(row['relevance'])
})
response = {
'relevance_score': relevance_score,
'for_you': posts,
'trending': [],
'following': []
}
return jsonify(response)