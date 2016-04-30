from asset import db, app
from datetime import datetime, date
from sqlalchemy.ext.declarative import declared_attr
from flask.ext.login import UserMixin


class AppMixin(object):
    """ Mixin class for general attributes and functions """

    @declared_attr
    def date_created(cls):
        return db.Column(db.DateTime, default=datetime.utcnow, index=True)

    @declared_attr
    def last_updated(cls):
        return db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)


class User(AppMixin, UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200), unique=True)
    full_name = db.Column(db.String(200), unique=False)
    password = db.Column(db.Text, unique=False)
    active = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_staff = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_super_admin = db.Column(db.Boolean, default=False)
    gender = db.Column(db.String(200))
    location = db.Column(db.String(200))

    def __repr__(self):
        return '<User %r>' % self.username


    def get_auth_token(self):
        """ Returns the user's authentication token """
        return hashlib.md5("%s:%s" % (self.username, self.password)).hexdigest()


    def is_active(self):
        """ Returns if the user is active or not. Overriden from UserMixin """
        return self.active


    def generate_password(self, password):
        """
        Generates a password from the plain string

        :param password: plain password string
        """

        self.password = bcrypt.generate_password_hash(password)


    def check_password(self, password):
        """
        Checks the given password against the saved password

        :param password: password to check
        :type password: string

        :returns True or False
        :rtype: bool

        """
        logger.info(self.password)
        logger.info(password)

        logger.info(bcrypt.check_password_hash(self.password, password))
        return bcrypt.check_password_hash(self.password, password)

    def set_password(self, new_password):
        """
        Sets a new password for the user

        :param new_password: the new password
        :type new_password: string
        """

        self.generate_password(new_password)
        db.session.add(self)
        db.session.commit()


class Consumer(AppMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    devices = db.relationship('Device', backref='consumer', lazy='dynamic')
    utility_provider_id = db.Column(db.Integer, db.ForeignKey('utility_provider.id'), nullable=False)


class UtilityProvider(AppMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=True)
    devices = db.relationship('Device', backref='utility_provider', lazy='dynamic')
    consumers = db.relationship('Consumer', backref='utilty_provider', lazy='dynamic')


class Device(AppMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference_id = db.Column(db.String, nullable=False)
    meter_reference_id = db.Column(db.String, nullable=True)
    consumer_id = db.Column(db.Integer, db.ForeignKey('consumer.id'), nullable=True)
    utility_provider_id = db.Column(db.Integer, db.ForeignKey('utility_provider.id'), nullable=True)
    is_master = db.Column(db.Boolean, default=False)
    is_slave = db.Column(db.Boolean, default=True)
    transformer_id = db.Column(db.Integer, db.ForeignKey('transformer.id'), nullable=True)
    transformer = db.relationship('Transformer', foreign_keys='Device.transformer_id')


class Transformer(AppMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_number = db.Column(db.String, nullable=False)
    capacity = db.Column(db.Float, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=True)


class Address(AppMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line1 = db.Column(db.String, nullable=False)
    line2 = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)


class Reading(AppMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.Float, default=27.0)
    transformer_id = db.Column(db.Integer, db.ForeignKey('transformer.id'), nullable=True)
    voltage = db.Column(db.Float, default=0.0)
    current = db.Column(db.Float, default=0.0)
    power = db.Column(db.Float, default=0.0)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)


class City(AppMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    code = db.Column(db.String(200))
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)


class State(AppMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    code = db.Column(db.String(200))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    cities = db.relationship('City', backref='state', lazy='dynamic')


class Country(AppMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    code = db.Column(db.String(200))
    states = db.relationship('State', backref='country', lazy='dynamic')
