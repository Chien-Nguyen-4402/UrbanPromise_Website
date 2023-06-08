from gunicorn.app.base import BaseApplication
from copy_app import app

class MyApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key, value)

    def load(self):
        return self.application

if __name__ == '__main__':
    # Replace 'cert.pem' and 'key.pem' with the actual paths to your SSL certificate and private key files
    # Update the 'bind' parameter to specify the host and port you want to listen on
    options = {
        'bind': '0.0.0.0:5000',
        'certfile': 'render_stuff/cert.pem',
        'keyfile': 'render_stuff/key.pem',
    }
    MyApplication(app, options).run()
