# -*- coding: utf-8 -*-
"""9755"""

import argparse

from app import app_
from blueprints import register_bp


register_bp(app_)


@app_.before_request
def before():
    """before
    """
    # g.start = time.clock()
    pass


@app_.teardown_request
def shutdown_session(exception=None):
    # current_session.remove()
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # 端口
    parser.add_argument('--port', help='端口. ',
                        type=int, default=9755)
    args = parser.parse_args()
    print('应用端口:', args.port)

    app_.run(host='0.0.0.0', port=args.port, use_reloader=False)
