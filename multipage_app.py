"""Multipage Dash app built using the link below as a start.

https://medium.com/@mcmanus_data_works/how-to-create-a-multipage-dash-app-261a8699ac3f
"""

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

from untracked_config.laminator_popup_links import lam_addresses


def create_navbar(*args, **kwargs):
    """Create the Dash navigation bar."""

    lam_links = [dbc.DropdownMenuItem(name, href=address) for (name, address) in lam_addresses.items()]

    navbar = dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu",
                align_end=True,
                children=[  # Add as many menu items as you need
                    dbc.DropdownMenuItem("Home", href='/dashboard'),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Defects Table", href='/dashboard/defects'),
                    dbc.DropdownMenuItem("Laminator Operators", href='/dashboard/operators'),
                    *lam_links,
                    dbc.Button(
                        # dbc.NavLink(
                        ["Logout"],
                        href="/dashboard/logout",
                    )
                ],
            ),
            dcc.Link(
                ["Logout"],
                href="/dashboard/logout",
                className='nav-link',
                target="_blank",

            ),
        ],
        brand='Nitto',
        brand_href="/",
        color="dark",  # Change this to change color of the navbar e.g. "primary", "secondary" etc.
        dark=True,  # Change this to change color of text within the navbar (False for dark text)
    )
    return navbar


def generate_dash_multipage_layout(*args, **kwargs):
    """Generate the layout for multiple Dash 'pages' in one."""
    navbar = create_navbar()
    return dcc.Loading(
        id='loading_page_content',
        children=[
            html.Div(
                [
                    navbar,
                    dash.page_container
                ]
            )
        ],
        color='primary',
        fullscreen=True
    )


if __name__ == '__main__':
    # To use Font Awesome Icons
    FA621 = "https://use.fontawesome.com/releases/v6.2.1/css/all.css"
    APP_TITLE = "Nitto Lakewood Dash App"
    app = dash.Dash(
        __name__,
        # suppress_callback_exceptions=True,
        external_stylesheets=[
            # Toggle the themes at [dbc.themes.LUX]
            # The full list of available themes is:
            # BOOTSTRAP, CERULEAN, COSMO, CYBORG, DARKLY, FLATLY, JOURNAL, LITERA, LUMEN,
            # LUX, MATERIA, MINTY, PULSE, SANDSTONE, SIMPLEX, SKETCHY, SLATE, SOLAR,
            # SPACELAB, SUPERHERO, UNITED, YETI, ZEPHYR.
            # To see all themes in action visit:
            # https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/explorer/
            dbc.themes.LUX,  # Dash Themes CSS
            FA621,  # Font Awesome Icons CSS
        ],
        title=APP_TITLE,
        use_pages=True,  # New in Dash 2.7 - Allows us to register pages
        pages_folder='pages'
    )
    app.layout = generate_dash_multipage_layout()

    server = app.server
    app.run_server(debug=False, use_reloader=True)

# TODO: * register callback in multipage layout
#       * merge multipage and flask + security into one
#       * fix defect latest date not updating after server start
