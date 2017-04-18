# encoding: utf-8

from werkzeug.utils import import_string

from ext import create_app

# 调试模式
DEBUG = True
app = create_app(debug=False)

blueprints = [
    'views.wx:bp'
]

for bp in blueprints:
    bp = import_string(bp)
    app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=DEBUG)
