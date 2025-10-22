from flask import Blueprint, current_app, jsonify, request
from utils.analytics import pattern_rules


patterns_bp = Blueprint('patterns', __name__)


@patterns_bp.route('/top')
def top_patterns():
limit = int(request.args.get('limit', 50))
ds = current_app.config['DATASTORE']
res = pattern_rules(ds, limit=limit)
return jsonify(res)


@patterns_bp.route('/graph')
def graph():
# simple: return topic co-occurrence edges computed in analytics if needed
ds = current_app.config['DATASTORE']
rules = pattern_rules(ds, limit=200, min_cooccurrence=2)
# build nodes and edges
nodes = []
edges = []
topics = list(ds.topics.keys())
nodes = [{'id': t, 'label': t, 'size': ds.topics[t]['total_mentions']} for t in topics]
# approximate edges from rules by parsing topic names
for r in rules:
# r['rule'] format: "<topic> often appears with phrase '...'", use heuristic
# skip detailed parsing here; include example: connect topic to itself with score
pass
return jsonify({'nodes': nodes, 'edges': edges})