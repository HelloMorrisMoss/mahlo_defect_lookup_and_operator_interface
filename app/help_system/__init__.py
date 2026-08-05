from flask import Blueprint

help_system_bp = Blueprint('help_system', __name__, 
                            template_folder='flask_server_files/templates',
                            static_folder='flask_server_files/static',
                            static_url_path='/help_system/static')

from app.help_system import routes
