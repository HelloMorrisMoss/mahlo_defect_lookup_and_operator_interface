"""Start the flask app."""

from app import create_app

server = create_app()

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5001, debug=True)
