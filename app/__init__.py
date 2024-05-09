import dash
from flask import Flask
from flask_login import login_required

from config import BaseConfig
from multipage_app import dash_multipage_layout


def create_app():
    server = Flask(__name__)
    server.config.from_object(BaseConfig)

    register_dashapps(server)
    register_extensions(server)
    register_blueprints(server)

    return server


def register_dashapps(app):
    from app.dashapp1.layout import layout
    from app.dashapp1.callbacks import register_callbacks

    # Meta tags for viewport responsiveness
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    # dashapp1 = dash.Dash(__name__,
    #                      server=app,
    #                      url_base_pathname='/dashboard/',
    #                      assets_folder=get_root_path(__name__) + '/dashboard/assets/',
    #                      meta_tags=[meta_viewport])
    #
    # with app.app_context():
    #     dashapp1.title = 'Dashapp 1'
    #     dashapp1.layout = layout
    #     register_callbacks(dashapp1)
    #
    # _protect_dashviews(dashapp1)
    # dashapp1 = dash.Dash(__name__,
    #                      server=app,
    #                      url_base_pathname='/dashboard/',
    #                      assets_folder=get_root_path(__name__) + '/dashboard/assets/',
    #                      meta_tags=[meta_viewport])

    import dash_bootstrap_components as dbc
    # To use Font Awesome Icons
    FA621 = "https://use.fontawesome.com/releases/v6.2.1/css/all.css"
    APP_TITLE = "Nitto Lakewood Dash App"
    dashapp1 = dash.Dash(
        __name__,
        # suppress_callback_exceptions=True,
        external_stylesheets=[
            dbc.themes.LUX,  # Dash Themes CSS
            FA621,  # Font Awesome Icons CSS
        ],
        title=APP_TITLE,
        use_pages=True,  # New in Dash 2.7 - Allows us to register pages
        pages_folder='pages',
        meta_tags=[meta_viewport],
        url_base_pathname='/dashboard/',
        # assets_folder=get_root_path(__name__) + '/dashboard/assets/',
    )

    with app.app_context():
        dashapp1.title = APP_TITLE
        dashapp1.layout = dash_multipage_layout
        register_callbacks(dashapp1)

    _protect_dashviews(dashapp1)


def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(
                dashapp.server.view_functions[view_func])


def register_extensions(server):
    from app.extensions import db
    from app.extensions import login
    from app.extensions import migrate

    db.init_app(server)
    login.init_app(server)
    login.login_view = 'main.login'
    migrate.init_app(server, db)


def register_blueprints(server):
    from app.webapp import server_bp

    server.register_blueprint(server_bp)
