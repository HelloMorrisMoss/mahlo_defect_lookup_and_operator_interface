# from dash import html, register_page, dcc
#
# app.layout = html.Div([ dcc.Location(id='url', refresh=False),
#                                      html.Div(id='page-content')
#                                     ]
#                                    )
#
# @app.callback(Output('page-content', 'children'),
#                        [Input('url', 'pathname')])
# def generate_layout(url):
#      """ url:  not a full url, but just the part after the host ip and port.
#                   ex:  [full url] http://my-dash-server:8080/username=duncan&userid=1234&graphsettings=23]
#                          [actual url string:   /username=duncan&userid ... ]
#      """
#      if not url: url='/'
#      config = dict(urllib.parse.parse_qsl(url.strip('/')))
#      ### alternative way to parse url
#      #config = urllib.parse.parse_qs(url)
#
#      return generate_content(config)
#
# def generate_content(config):
#     """ Uses config dictionary as parameters to generate a list of html or dcc components """
#     return []
