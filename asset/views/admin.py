import os
from flask import Blueprint, render_template, redirect, url_for, request, session, abort
from flask_login import login_required, login_user, logout_user
from datetime import datetime, date
from asset.forms import *
from asset.services.users import authenticate_user
from asset.models import *
from asset.services.assets import DeviceService, TransformerService
from sqlalchemy import asc, desc, or_, and_, func

main = Blueprint('main', __name__, template_folder="templates")


@main.errorhandler(404)
def page_not_found(e):
    page_title = "404- Page Not Found"
    error_code = "404"
    error_title = "Sorry Page not found!"
    error_info = "The requested page cannot be found or does not exist. Please contact the Administrator."

    return render_template('error.html', **locals()), 404


# @main.errorhandler(500)
# def internal_server_error(e):
#     page_title = "500- Internal Server Error"
#     error_code = "500"
#     error_title = "Sorry there has been a Server Error!"
#     error_info = "There has been an Internal server Error. Please try again later or Contact the Administrator."
#
#     return render_template('main/error.html', **locals()), 500


@main.context_processor
def main_context():
    """ Include some basic assets in the startup page """
    today = date.today()
    current_year = today.strftime('%Y')

    return locals()


@main.route('/login/', methods=["GET", "POST"])
def login():
    page_title = "Log In"

    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        data = form.data
        username = data["username"]
        password = data["password"]

        user = authenticate_user(username, password)

        if user and user.deactivate:
        	login_error = "User has been deactivated. Please contact support team."
        else:
        	if user is not None:

        		login_user(user, remember=True, force=True) # This is necessary to remember the user

        		identity_changed.send(app, identity=Identity(user.id))

        		resp = redirect(url_for('.index'))

        		# Transfer auth token to the frontend for use with api requests
        		__xcred = base64.b64encode("%s:%s" % (user.username, user.get_auth_token()))

        		resp.set_cookie("__xcred", __xcred)

        		return resp

        	else:
        		login_error = "The username or password is invalid"

    return render_template("login.html", **locals())


@main.route('/logout/')
def logout():
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(app, identity=AnonymousIdentity())

    return redirect(url_for('.page'))

@login_required
@main.route('/', methods=["GET", "POST"])
def index():
    page_title = "Home"
    page_caption = "General Admin Dashboard"
    if request.method == "POST":
        pass
    return render_template('index.html', **locals())


@login_required
@main.route('/devices/')
def devices():
    page_title="Devices"
    page_caption = "List of All Devices"

    try:
        page = int(request.args.get("page",1))
        search_q = request.args.get("q",None)
    except:
        abort(404)

    query = Device.query

    if search_q:
        queries = [Device.reference_code.ilike("%%%s%%"%search_q), Device.meter_reference_code.ilike("%%%s%%"%search_q)]
        query = query.filter(or_(*queries))

    results = query.order_by(desc(Device.date_created)).paginate(page, 20, False)

    return render_template('/lists/devices.html', **locals())


@login_required
@main.route('/devices/register/', methods=["GET","POST"])
def create_device():
    page_title="Register A Device"
    page_caption = ""

    form = DeviceForm(csrf_enabled=False)
    form.consumer_id.choices = [(c.id, c.name) for c in Consumer.query.all()]
    form.transformer_id.choices = [(c.id, c.name) for c in Transformer.query.all()]
    form.utility_provider_id.choices = [(c.id, c.name) for c in UtilityProvider.query.all()]

    if form.validate_on_submit():
        device = DeviceService.create(ignored_args=None, **form.data)
        return redirect(url_for('.devices'))

    return render_template('/forms/devices.html', **locals())


@main.route('/devices/<int:id>/analysis/', methods=["GET","POST"])
def device(id):
    page_title="Device"
    page_caption=""
    return render_template('/details/device.html', **locals())


@main.route('/transformers/')
def transformers():
    page_title="Transformers"
    page_caption = "List of All Transformers"

    try:
        page = int(request.args.get("page",1))
        search_q = request.args.get("q",None)
    except:
        abort(404)

    query = Transformer.query

    if search_q:
        queries = [Transformer.model_number.ilike("%%%s%%"%search_q), Transformer.capacity.ilike("%%%s%%"%search_q)]
        query = query.filter(or_(*queries))

    results = query.order_by(desc(Transformer.date_created)).paginate(page, 20, False)

    return render_template('/lists/transformers.html', **locals())


@main.route('/transformers/register/', methods=["GET","POST"])
def create_transformer():
    page_title="Register A Transformer"
    page_caption = ""

    form = TransformerForm(csrf_enabled=False)
    
    if form.validate_on_submit():
        transformer = TransformerService.create(ignored_args=None, **form.data)
        return redirect(url_for('.transformers'))
        
    return render_template('/forms/transformers.html', **locals())
