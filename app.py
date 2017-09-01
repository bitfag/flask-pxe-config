from flask import Flask
app = Flask(__name__)

from flask import render_template
from flask import request

import re

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    filename = request.form['MAC'].replace(':', '-')
    path = 'out/' + filename

    mac = request.form['MAC']
    rbd = request.form['rbd device']
    if re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):

        try:
            f = open(path, 'w')
            f.write(render_template('config.tmpl', mac=mac, rbd=rbd, config_path=path))
            f.close()
        except Exception as e:
            return 'Failed to write to file "%s"<br /> reason: "%s"' % (path, e)

        return render_template('generate.html', mac=mac, rbd=rbd, config_path=path)

    else:
        error = 'Invalid MAC address format'
        return render_template('index.html', error=error)
