"""Start the flask app."""
from datetime import datetime

import waitress

from app import create_app

server = create_app()

if __name__ == '__main__':
    port = 5001
    host = '0.0.0.0'
    print(f'{datetime.now()} - Serving on: {host}:{port}')
    waitress.serve(server, host=host, port=port, threads=2)
    # server.run(port=port, host=host, use_reloader=True)
