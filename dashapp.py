"""Start the flask app."""

import waitress

from app import create_app

server = create_app()

if __name__ == '__main__':
    waitress.serve(server, host='0.0.0.0', port=5001, threads=2)
