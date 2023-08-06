#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import requests
import re
import sys
import json
import logging
import keyword
import string
import random
import pkg_resources
from dateutil.parser import parse
from pytz import utc
from functools import wraps
from pathlib import Path

log = logging.getLogger('yams-client')


def configure_logging(loglevel, logfile=None):
    """ Configure logging to the defined level using (if provided) a file.
    :param loglevel: logging level
    :param logfile: file to write the logs
    :return:
    """
    loglevel = loglevel.upper()
    loglevels = ('DEBUG', 'INFO', 'WARNING', 'ERROR')
    if loglevel not in loglevels:
        raise Exception('"loglevel" must be one of {}'.format(loglevels))

    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s - %(message)s',
        datefmt='%m-%d %H:%M:%S',
        level=loglevel,
        stream=sys.stderr)


def retrieve_action(options, allowed_commands):
    """ Given the cli input options, return the one to be executed.
    :param options:
    :param allowed_commands:
    :return:
    """
    actions = filter(lambda opt: not opt.startswith('<') and not opt.startswith('-') and opt in allowed_commands,
                     options.keys())

    for action in actions:
        if options[action]:
            action = action.replace('-', '_')
            if keyword.iskeyword(action):
                action = '{}_'.format(action)
            return action


def is_action_confirmed(element_id, command, action):
    msg = 'Trying to {} the {} id {}. Should we proceed?'.format(action, command, element_id)
    return input("%s (y/N) " % msg).lower() == 'y'


def exception_safe(exception):
    """
    Catch the exception, log it and return a value
    """

    def decorator(func):
        def wrapper(*args, **kwds):
            try:
                return func(*args, **kwds)
            except exception as e:
                log.error("A '{}' occurred: {}".format(type(e).__name__, e))

        return wrapper

    return decorator


def dispatcher_exception_safe(exception):
    """
    Catch the exception, log it and return a value
    """

    def decorator(func):
        def wrapper(*args, **kwds):
            try:
                return func(*args, **kwds)
            except exception as e:
                log.error("A '{}' occurred".format(type(e).__name__))
                if hasattr(e, "message"):
                    print(e.message)
                else:
                    print(e)
                return False

        return wrapper

    return decorator


def format_upgrade_msg(current_version, latest_version):
    return f"The current yams-cli version is {current_version}, but a newer one ({latest_version}) is available. Please consider upgrading."


def latest_version_warning(func):
    """
    In happy path will print in stderr if the cli is not the latest version
    In the case of any error we are not going to print do anything
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_version = get_version()
        latest_version = get_latest_version()
        if latest_version and latest_version != current_version:
            log.info(format_upgrade_msg(current_version=current_version, latest_version=latest_version))
        return func(*args, **kwargs)

    return wrapper


def generate_pretty_print(content):
    """ Pretty printing the json content.
    :param content:
    :return:
    """
    return json.dumps(content, sort_keys=True, indent=4, separators=(',', ': '))


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """ Generates a random string.
    :param size: integer. Resulting random string length
    :param chars: characters list. Input characters to generate the random string
    :return:
    """
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def get_directory(filename):
    directories = filename.split("/")
    directory = ""
    for i in range(len(directories) - 1):
        directory += directories[i] + "/"
    return directory


def valid_uuid(uuid):
    regex = re.compile(r'^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}\Z', re.I)
    match = regex.match(uuid)
    return bool(match)


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def get_version():
    try:
        version = pkg_resources.require("yams-cli")[0].version
    except pkg_resources.ResolutionError:
        version = '0.0.1'

    return version


def fetch_latest_pypi_version():
    """
    fetches the public pypi page
    attempts to parse the html to find the cli version
    returns the latest cli version if available
    in case of any failure it returns None
    """
    PYPY_URL = 'https://pypi.org/pypi/yams-cli/json' 
    TIMEOUT_SECONDS = 1
    try:
        r = requests.get(url=PYPY_URL, timeout=TIMEOUT_SECONDS)
        status = r.status_code
        if status != 200: 
            return None

        body = r.json()
        yams_version =  body["info"]["version"]
        return yams_version
    except: 
        return None


def get_latest_version(
        file_path =  Path.home() / '.yams/.version',
        threshold_seconds = 86400, # 1 day = 86400 seconds
        fetch_latest_from = fetch_latest_pypi_version
    ):
    """
    Attempts to get the latest version from file or pypi.
    Returns None if failure
    """
    YAMS_VERSION_PATH = file_path
    THRESHOLD_SECONDS = threshold_seconds
    FETCH_LATEST_VERSION = fetch_latest_from

    def _write_file(latest_version):
        with open(YAMS_VERSION_PATH, mode='w') as f:
            print(latest_version, file=f)

    def _read_file_version():
        with open(YAMS_VERSION_PATH, mode='r') as f:
            file_version = f.readline().strip()
            return file_version
    
    try:
        if os.path.exists(YAMS_VERSION_PATH):
            file_last_modified_time = YAMS_VERSION_PATH.lstat().st_mtime 
            host_current_time = time.time()
            if host_current_time > file_last_modified_time + THRESHOLD_SECONDS:
                latest_version = FETCH_LATEST_VERSION()
                if latest_version:
                    _write_file(latest_version)
                return latest_version
            else:
                return _read_file_version()
        else:
            latest_version = FETCH_LATEST_VERSION()
            if latest_version:
                open(os.path.abspath(YAMS_VERSION_PATH), 'a').close()
                _write_file(latest_version)
            return latest_version
    except:
        return None


def is_date(text, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param text: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        date = parse(text, fuzzy=fuzzy)
        return date.replace(tzinfo=utc), True
    except Exception:
        return None, False


def get_timestamp(text):
    (date, is_valid_date) = is_date(text)
    if not is_valid_date:
        return int(text)
    else:
        return int(date.timestamp())


def is_not_blank(my_string):
    return bool(my_string and my_string.strip())
