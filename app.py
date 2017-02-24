#! /bin/python3.5

from src.app import app
from src import views

import os

if __name__ == '__main__':
    app.run(host='0.0.0.0', 
            port=os.environ.get('FTMP3_PORT', 5000))

