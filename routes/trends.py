from flask import Blueprint, current_app, jsonify, request
from utils.analytics import analyze_trends, platform_comparison


trends_bp = Blueprint('trends', __name__)


@trends_bp.route('/overview')
def overview():
days = int(request.args.get('days', 90))
ds = current_app.config['DATASTORE']
res = analyze_trends(ds, days=days)
return jsonify(res)




@trends_bp.route('/platform-comparison')
def platform_comp():
topic = request.args.get('topic')
start = request.args.get('start')
end = request.args.get('end')
ds = current_app.config['DATASTORE']
res = platform_comparison(ds, topic, start=start, end=end)
return jsonify(res)