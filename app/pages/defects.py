from dash import register_page  # , callback # If you need callbacks, import it here.

register_page(
    __name__,
    name='Defects',
    top_nav=True,
    path='/defects'
)


def layout():
    from app.dashapp1.layout import layout as defect_layout

    return defect_layout
