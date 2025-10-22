from flask import Blueprint, current_app, jsonify, request


from utils.analytics import topic_time_series


topics_bp = Blueprint('topics', __name__)


@topics_bp.route('/list')
def list_topics():
q = request.args.get('query','').lower()
limit = int(request.args.get('limit',20))
ds = current_app.config['DATASTORE']
topics = []
for t,meta in ds.topics.items():
if q and q not in t.lower():
continue
topics.append({'topic': t, 'total_mentions': meta['total_mentions'], 'last_updated': str(meta['last_updated'])})
if len(topics)>=limit:
break
return jsonify({'topics': topics})


@topics_bp.route('/detail')
def topic_detail():
topic = request.args.get('topic')
ds = current_app.config['DATASTORE']
if topic not in ds.topics:
return jsonify({'error':'topic not found'}), 404
series = topic_time_series(ds, topic)
# sample posts
posts = ds.df[ds.df['topic']==topic].sort_values('timestamp', ascending=False).head(10).to_dict('records')
return jsonify({'topic': topic, 'time_series': series, 'sample_posts': posts})