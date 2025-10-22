from flask import Blueprint, current_app, jsonify, request
from utils.analytics import pattern_rules

patterns_bp = Blueprint('patterns', __name__)

@patterns_bp.route('/top')
def top_patterns():
    """Identifies and returns top co-occurrence patterns between topics and phrases."""
    limit = int(request.args.get('limit', 50))
    ds = current_app.config['DATASTORE']

    if ds.df.empty:
        return jsonify([])

    res = pattern_rules(ds, limit=limit)
    return jsonify(res)

@patterns_bp.route('/graph')
def graph():
    """Generates data for a topic co-occurrence network graph."""
    ds = current_app.config['DATASTORE']

    if ds.df.empty:
        return jsonify({'nodes': [], 'edges': []})
        
    # Use a higher limit for better graph connectivity, but keep it reasonable
    rules = pattern_rules(ds, limit=100, min_cooccurrence=2)
    
    # Build nodes and edges
    topics = list(ds.topics.keys())
    nodes = [{'id': t, 'label': t, 'size': ds.topics.get(t, {}).get('total_mentions', 0)} for t in topics]

    # Approximate edges from rules by parsing topic names
    # This is a simple heuristic; a more advanced approach might use NLP to extract entities
    edges = []
    edge_counts = {} # To aggregate weights
    
    for r in rules:
        rule_text = r.get('rule', '')
        # Simple heuristic to find topic co-occurrence
        for t1 in topics:
            if t1 in rule_text:
                 for t2 in topics:
                     if t2 in rule_text and t1 != t2:
                         # Create a consistent key for each pair to avoid duplicate edges
                         edge_key = tuple(sorted((t1, t2)))
                         if edge_key not in edge_counts:
                             edge_counts[edge_key] = 0
                         edge_counts[edge_key] += r.get('cooccurrence_count', 0)
    
    for (source, target), weight in edge_counts.items():
        edges.append({'source': source, 'target': target, 'weight': weight})


    return jsonify({'nodes': nodes, 'edges': edges})