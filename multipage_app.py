"""

https://medium.com/@mcmanus_data_works/how-to-create-a-multipage-dash-app-261a8699ac3f
"""

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc


# from navbar import create_navbar

# Toggle the themes at [dbc.themes.LUX]
# The full list of available themes is:
# BOOTSTRAP, CERULEAN, COSMO, CYBORG, DARKLY, FLATLY, JOURNAL, LITERA, LUMEN,
# LUX, MATERIA, MINTY, PULSE, SANDSTONE, SIMPLEX, SKETCHY, SLATE, SOLAR,
# SPACELAB, SUPERHERO, UNITED, YETI, ZEPHYR.
# To see all themes in action visit:
# https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/explorer/


def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(
                dbc.NavLink(
                    [
                        html.I(className="fa-brands fa-github"),  # Font Awesome Icon
                        " "  # Text beside icon
                    ],
                    href="[YOUR GITHUB PROFILE URL]",
                    target="_blank"
                )

            ),
            dbc.NavItem(
                dbc.NavLink(
                    [
                        html.I(className="fa-brands fa-medium"),  # Font Awesome Icon
                        " "  # Text beside icon
                    ],
                    href="[YOUR MEDIUM PROFILE URL]",
                    target="_blank"
                )

            ),
            dbc.NavItem(
                dbc.NavLink(
                    [
                        html.I(className="fa-brands fa-linkedin"),  # Font Awesome Icon
                        " "  # Text beside icon
                    ],
                    href="[YOUR LINKEDIN PROFILE URL]",
                    target="_blank"
                )

            ),
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu",
                align_end=True,
                children=[  # Add as many menu items as you need
                    dbc.DropdownMenuItem("Home", href='/'),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Defects Table", href='/defects'),
                    dbc.DropdownMenuItem("Laminator Operators", href='/operators'),
                ],
            ),
        ],
        brand='Nitto',
        brand_href="/",
        # sticky="top",  # Uncomment if you want the navbar to always appear at the top on scroll.
        color="dark",  # Change this to change color of the navbar e.g. "primary", "secondary" etc.
        dark=True,  # Change this to change color of text within the navbar (False for dark text)
    )

    return navbar


navbar = create_navbar()

# # To use if you're planning on using Google Analytics
# app.index_string = f'''
# <!DOCTYPE html>
# <html>
#     <head>
#         {{%metas%}}
#         <title>{APP_TITLE}</title>
#         {{%favicon%}}
#         {{%css%}}
#     </head>
#     <body>
#         {{%app_entry%}}
#         <footer>
#             {{%config%}}
#             {{%scripts%}}
#             {{%renderer%}}
#         </footer>
#
#     </body>
# </html>
# '''

dash_multipage_layout = dcc.Loading(  # <- Wrap App with Loading Component
    id='loading_page_content',
    children=[
        html.Div(
            [
                navbar,
                dash.page_container
            ]
        )
    ],
    color='primary',  # <- Color of the loading spinner
    fullscreen=True  # <- Loading Spinner should take up full screen
)

if __name__ == '__main__':
    # To use Font Awesome Icons
    FA621 = "https://use.fontawesome.com/releases/v6.2.1/css/all.css"
    APP_TITLE = "Nitto Lakewood Dash App"
    app = dash.Dash(
        __name__,
        # suppress_callback_exceptions=True,
        external_stylesheets=[
            dbc.themes.LUX,  # Dash Themes CSS
            FA621,  # Font Awesome Icons CSS
        ],
        title=APP_TITLE,
        use_pages=True,  # New in Dash 2.7 - Allows us to register pages
        pages_folder='pages'
    )

    app.layout = dash_multipage_layout

    server = app.server
    app.run_server(debug=False, use_reloader=True)

# TODO: * register callback in multipage layout
#       * merge multipage and flask + security into one
#       * fix defect latest date not updating after server start
