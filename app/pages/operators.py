from dash import register_page

register_page(
    __name__,
    name='Operators',
    top_nav=True,
    path='/operators'
)


def layout():
    from app.operators_app.layout import get_operator_layout

    return get_operator_layout()
