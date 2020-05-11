# -*- coding: utf-8 -*-
"""blueprints
"""

from business.front.routes import rf_front


def register_bp(app_):
    """register bp
    """
    app_.register_blueprint(rf_front)
