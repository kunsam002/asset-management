"""
services.py

@Author: stikks and kunsam002


"""

import re
import json
from unicodedata import normalize
from datetime import datetime, date, timedelta
from email.utils import formatdate
from calendar import timegm
from user_agents import parse
import requests
import os
import base64
import cStringIO
import string
import random
import phonenumbers
import hashlib
import math


_slugify_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


class DateJSONEncoder(json.JSONEncoder):
    """ JSON Encoder class to support date and time encoding """

    def default(self, obj):
        if isinstance(obj, datetime):
            return formatdate(timegm(obj.utctimetuple()), usegmt=True)

        if isinstance(obj, date):
            _obj = datetime.combine(obj, datetime.min.time())
            return formatdate(timegm(_obj.utctimetuple()), usegmt=True)

        return json.JSONEncoder.default(self, obj)


def expand_errors(data):
    """ Cleans up the error data of forms to enable proper json serialization """
    res = {}
    for k, v in data.items():
        tmp = []
        for x in v:
            tmp.append(str(x))
        res[k] = tmp

    return res


def slugify(text, delim=u'-'):
    """
    Generates an ASCII-only slug.

    :param text: The string/text to be slugified
    :param: delim: the separator between words.

    :returns: slugified text
    :rtype: unicode
    """

    result = []
    for word in _slugify_punct_re.split(text.lower()):
        # ensured the unicode(word) because str broke the code
        word = normalize('NFKD', unicode(word)).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))


def normalize_text(text):

    """
    Generates an ASCII-only text
    :rtype: str
    """
    if text:
        result = []
        for word in text:
            # ensured the unicode(word) because str broke the code
            word = normalize('NFKD', unicode(word)).encode('ascii', 'ignore')
            if word:
                result.append(word)
        return unicode(''.join(result))


def clean_kwargs(ignored_keys, data):
    """
    Removes the ignored_keys from the data sent

    :param ignored_keys: keys to remove from the data (list or tuple)
    :param data: data to be cleaned (dict)

    returns: cleaned data
    rtype: dict
    """

    for key in ignored_keys:
        data.pop(key, None)

    return data


def populate_obj(obj, data):
    """
    Populates an object with the data passed to it

    :param obj: Object to be populated
    :param data: The data to populate it with (dict)

    :returns: obj populated with data
    :rtype: obj.__class__

    """
    for name, value in data.items():
        if hasattr(obj, name):
            setattr(obj, name, value)

    return obj


def remove_invalid_attributes(obj, data):
    """ remove the attributes of a dictionary that do not belong in an object """
    _data = {}
    for name, value in data.items():
        if hasattr(obj, name):
            _data[name] = value

    return _data


def validate_data_keys(data, keys):
    """
    Check the data dictionary that all the keys are present within it
    """
    for k in keys:
        if not data.has_key(k):
            raise Exception("Invalid data. All required parameters need to be present. Missing Key: [%s]" % k)

    return data


def copy_dict(source, dest):
    """
    Populates a destination dictionary with the values from the source

    :param source: source dict to read from
    :param dest: destination dict to write to

    :returns: dest
    :rtype: dict

    """
    for name, value in source.items():
        dest[name] = value
    return dest


def remove_empty_keys(data):
    """ removes None value keys from the list dict """
    res = {}

    for key, value in data.items():
        if value is not None:
            res[key] = value

    return res


def detect_user_agent(ua_string):
    """
    Detects what kind of device is being used to access the server
    based on the user agent

    :param ua_string: The user agent string to parse

    :returns: user agent object
    """

    ua = parse(ua_string)

    return ua


def prepare_errors(errors):
    _errors = {}
    for k, v in errors.items():
        _res = [str(z) for z in v]
        _errors[str(k)] = _res

    return _errors


def detect_user_device(ua_string):
    """ returns which device is used in reaching the application. 'm' for mobile, 'd' for desktop and 't' for tablet """

    ua = detect_user_agent(ua_string)

    device = "d"

    if ua.is_tablet:
        device = "t"

    if ua.is_mobile:
        device = "m"

    if ua.is_pc:
        device = "d"

    return device


def download_file(url, dest, filename):
    """
    Downloads a file from a url into a given destination
    and returns the location when it's done

    :param url: url to downlaod from
    :param dest: destination folder
    :param filename: filename to save the downloaded file as

    """

    r = requests.get(url)
    path = os.path.join(dest, filename)
    with open(path) as doc:
        doc.write(r.content)
    doc.close()
    return path


def id_generator(size=10, chars=string.ascii_letters + string.digits):
    """
    utility function to generate random identification numbers
    """
    return ''.join(random.choice(chars) for x in range(size)).upper()


def token_generator(size=8, chars=string.digits):
    """
    utility function to generate random identification numbers
    """
    return ''.join(random.choice(chars) for x in range(size))


def number_format(value):
    return "{:,.2f}".format(float(value))


def is_list(value):
    return isinstance(value, (list, tuple))


def md5_hash(value):
    """ create the md5 hash of the string value """
    return hashlib.md5(value).hexdigest()


def join_list(value, key):
    """ Iterate through a list and retrieve the keys from it """
    return ", ".join([getattr(x, key, "") for x in value])


def clean_phone(number, code):
    _number = code + str(number)

    return _number


def clean_phone_number(number, code):
    num = []
    chars = ['or', 'and', '/', ',']

    for char in chars:
        if char in number:

            number = number.replace(char, "").strip().split()

            count = 0

            _num = []

            while count < len(number):
                nos = number[count]
                nos = filter(lambda x: x.isdigit(), nos)

                if nos.startswith('234'):
                    nos = nos[3:]

                action = clean_phone(int(nos), code)
                _num.append(action)
                count += 1

            return _num

    number = filter(lambda x: x.isdigit(), number)

    if number.startswith('234'):
        number = number[3:]

    _number = clean_phone(int(number), code)
    num.append(_number)

    return num


def format_phone_numbers(raw_numbers, code):
    """
    Properly formats a list or string of phone numbers into the country code

    :param raw_numbers: Phone number to parse and format
    :param code: country code to utilize
    :return: properly formatted phone number or None
    """

    # Convert list or tuple to string if passed
    if isinstance(raw_numbers, (list, tuple)):
        raw_numbers = ','.join(raw_numbers)

    numbers = []
    for n in raw_numbers.replace("or", ","). \
            replace("\n", ","). \
            replace(".", ","). \
            replace("and", ","). \
            replace(";", ","). \
            replace("/", ",").split(","):
        if len(n) > 0:
            try:
                _n = phonenumbers.parse(n, code)
                if _n and phonenumbers.is_valid_number(_n):
                    cc = _n.country_code
                    nn = _n.national_number
                    num = str(cc) + str(nn)
                    numbers.append(num)
            except Exception, e:
                pass

    return numbers


def next_working_day(start_date, days):
    """ calculate the next working day from the start date over a period in days by removing all weekends between and appending them to the date """
    end = int(math.ceil(days + 1))
    days_involved = [(start_date + timedelta(days=x)).isoweekday() for x in range(1, end)]

    weekends = [x for x in days_involved if x in [6, 7]]
    off_days = len(weekends)
    days_without_weekends = start_date + timedelta(days=math.ceil(days))
    days_with_weekends = start_date + timedelta(days=math.ceil(days + off_days))

    if off_days == 0:
        return days_with_weekends
    else:
        return next_working_day(days_without_weekends, (days_with_weekends - days_without_weekends).days)



class ObjectNotFoundException(Exception):
    """ This exception is thrown when an object is queried by ID and not retrieved """

    def __init__(self, klass, obj_id):
        message = "%s: Object not found with id: %s" % (klass.__name__, obj_id)
        self.data = {"name": "ObjectNotFoundException", "message": message}
        self.status = 501
        super(ObjectNotFoundException, self).__init__(message)



class ServiceFactory(object):
    """
    Factory class for creating services. The service class will be bound to a model and returned as a class.
    This class can then be used or subclassed directly. The services generated by this class will contain
    specific methods for creating, retrieving, updating, deleting and querying data.
    """

    @classmethod
    def create_service(cls, klass, db):
        """
        :param cls: SQLAlchemy model class to be bound to service.

        This model will return
        """

        class BaseService:
            """ Generic class that contains all static/class methods required """

            def __init__(self):
                pass

            db = None
            query = None

            @classmethod
            def create(cls, ignored_args=None, **kwargs):
                """ Create the new model object and persist it. Execute possible pre/post method calls for audit and others """
                if not ignored_args:
                    ignored_args = ["id", "date_created", "last_updated"]

                obj = BaseService.model_class()
                data = clean_kwargs(ignored_args, kwargs)
                obj = populate_obj(obj, data)

                db.session.add(obj)
                try:
                    db.session.commit()
                    if hasattr(obj, "__search_class__"):
                        cls.index_object(obj)
                    return obj
                except:
                    db.session.rollback()
                    raise

            @classmethod
            def update(cls, obj_id, ignored_args=None, **kwargs):
                """ Update an existing model by obj_id and persist it. Execute """

                obj = BaseService.model_class.query.get(obj_id)

                if not obj:
                    raise ObjectNotFoundException(BaseService.model_class, obj_id)

                obj = db.session.merge(obj)
                if not ignored_args:
                    ignored_args = ["id", "date_created", "last_updated"]

                data = clean_kwargs(ignored_args, kwargs)
                obj = populate_obj(obj, data)
                db.session.add(obj)
                try:
                    db.session.commit()
                    return obj
                except:
                    db.session.rollback()
                    raise

            @classmethod
            def update_by_ids(cls, obj_ids, ignored_args=None, **kwargs):
                """ Execute bulk update on a group of objects selected by their ids """

                data = clean_kwargs(ignored_args, kwargs)
                data = remove_invalid_attributes(BaseService.model_class(), data)

                try:
                    res = cls.query.filter(cls.model_class.id.in_(obj_ids)).update(data, synchronize_session=False)
                    db.session.commit()
                    return res
                except Exception, e:
                    db.session.rollback()
                    raise

            @classmethod
            def get(cls, obj_id):
                """ Simple query method to get an object by obj_id """
                obj = cls.query.get(obj_id)

                if not obj:
                    raise ObjectNotFoundException(BaseService.model_class, obj_id)

                return obj

            @classmethod
            def delete(cls, obj_id):
                """ delete an object for the existing model by obj_id"""

                obj = cls.query.get(obj_id)
                obj = db.session.merge(obj)

                if not obj:
                    raise ObjectNotFoundException(BaseService.model_class, obj_id)

                db.session.delete(obj)
                try:
                    db.session.commit()
                    return True
                except:
                    db.session.rollback()
                    raise

            @classmethod
            def get_by_ids(cls, ids=None):
                """ Retrieve an array of objects specified by the ids """
                if not ids:
                    ids = []

                objects = cls.query.filter(cls.model_class.id.in_(ids))

                return objects

            @classmethod
            def delete_by_ids(cls, ids=None):
                """ Delete an array of objects specified by ids """
                if not ids:
                    ids = []
                for obj in cls.model_class.query.filter(cls.model_class.id.in_(ids)):
                    db.session.delete(obj)
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()
                        raise
                return True

        # Set the model class on the service
        BaseService.model_class = klass
        BaseService.db = db
        BaseService.query = klass.query

        return BaseService
