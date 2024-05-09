from dash import register_page  # , callback # If you need callbacks, import it here.

register_page(
    __name__,
    name='Operators',
    top_nav=True,
    path='/operators'
)


def layout():
    from scratch_4 import operator_layout

    return operator_layout
