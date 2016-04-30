import os
from flask import Blueprint, render_template
from datetime import datetime

main = Blueprint('main', __name__)


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
    today = datetime.today()
    current_year = today.strftime('%Y')

    return locals()


@main.route('/login/', methods=["GET", "POST"])
def login():
    page_title = "Log In"

    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        username = data["username"]
        password = data["password"]

        user = None

        # user = authenticate_buyer(username, password)

        # if user and user.deactivate:
        # 	login_error = "User has been deactivated. Please contact support team."
        # else:
        # 	if user is not None:

        # 		# if not user.is_setup:
        # 		# 	login_error = "User account not verified!"
        # 		# 	flash("Please check your email for Account verification.")
        # 		# 	resp = redirect(next_url_)
        # 		# 	return resp

        # 		login_user(user, remember=True, force=True) # This is necessary to remember the user

        # 		identity_changed.send(app, identity=Identity(user.id))

        # 		resp = redirect(next_url_)

        # 		# Transfer auth token to the frontend for use with api requests
        # 		__xcred = base64.b64encode("%s:%s" % (user.username, user.get_auth_token()))

        # 		resp.set_cookie("__xcred", __xcred)

        # 		return resp

        # 	else:
        # 		login_error = "The username or password is invalid"

        login_user(user, remember=True, force=True)  # This is necessary to remember the user

        identity_changed.send(app, identity=Identity(user.id))

        resp = redirect(url_for('.index'))

        # Transfer auth token to the frontend for use with api requests
        __xcred = base64.b64encode("%s:%s" % (user.username, user.get_auth_token()))

        resp.set_cookie("__xcred", __xcred)

        return resp

    return render_domain_template("user/login.html", **locals())


@main.route('/logout/')
def logout():
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(app, identity=AnonymousIdentity())

    return redirect(url_for('.page'))


@main.route('/')
def index():
    page_title = "Home"
    wrapper_class = "homepage homepage-1"
    return render_template('index.html', **locals())


@main.route('/devices/')
def devices():
    page_title="Devices"
    return render_template('/lists/demo.html', **locals())
