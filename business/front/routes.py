# -*- coding: utf-8 -*-
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import Blueprint
from flask import session as f_session
from flask_login import logout_user
from flask_login import login_required
from jinja2.exceptions import TemplateNotFound

from common.st_flog import error_un_excepted

rf_front = Blueprint('rf_front', __name__,
                     template_folder='templates')


@rf_front.route('/', methods=['get'], endpoint='/')
def home():
    """登录页面跳转"""
    return redirect(url_for('rf_front.home_html'))


@rf_front.route('/s/home.html', methods=['get'],
                defaults={'target': 'home.html'}, endpoint='home_html')
def home(target):
    """登录页面"""
    return render_template(target, **locals())


@rf_front.route('/s/<string:target>', defaults={'module': ''},
                methods=['get'], endpoint='without_module')
@rf_front.route('/s/<string:module>/<string:target>',
                methods=['get'], endpoint='with_module')
def load_target(module, target):
    """索引"""

    lo = {'target': target,
          'module': module,
          }

    try:
        __target = module + '/' + target if module else target
        return render_template(__target)
    except TemplateNotFound as e:
        error_un_excepted(
            m='页面不存在: %s, %s' % (request.path, e),
            lo=lo,
            func='load_target'
        )
        return redirect(url_for('rf_front.home_html'))
