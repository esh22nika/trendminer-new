from flask import Flask
from flask_cors import CORS
from routes.dashboard import dashboard_bp
from routes.trends import trends_bp
from routes.patterns import patterns_bp
from routes.topics import topics_bp
from utils.data_loader import DataStore




def create_app():
app = Flask(__name__)
CORS(app)


# Load data
app.config['DATASTORE'] = DataStore(csv_path='data/mock_social_trends_5000.csv')


# register blueprints
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
app.register_blueprint(trends_bp, url_prefix='/api/trends')
app.register_blueprint(patterns_bp, url_prefix='/api/patterns')
app.register_blueprint(topics_bp, url_prefix='/api/topics')


@app.route('/health')
def health():
return {'status': 'ok'}


return app