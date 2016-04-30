from asset import db, app

class AppMixin(object):
    """ Mixin class for general attributes and functions """

    @declared_attr
    def date_created(cls):
        return db.Column(db.DateTime, default=datetime.utcnow, index=True)


    @declared_attr
    def last_updated(cls):
        return db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)


class Device(AppMixin, db.Model):

	id = db.Column(db.Integer, primary_key=True)
	reference_id = db.Column(db.String, nullable=False)


class TemparatureRecord(AppMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	tempature = db.Column(db.Float, default=27.0)
	device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)


