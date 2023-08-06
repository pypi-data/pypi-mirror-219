from __future__ import absolute_import

import os.path
from os.path import relpath
import os
import re
from blendedUx.blended_flask.blended_hostlib.transform_image import TransformImage
from blendedUx.blended_flask.settings import *


def multiple_replace(replace_characters, text):
    """
    """
    pattern = "|".join(map(re.escape, replace_characters.keys()))
    return re.sub(pattern, lambda m: replace_characters[m.group()], text)


def save_css(path, content):
    """
    :param name:
    :param content:
    :return:
    """
    split_path = path.rsplit(os.sep, 1)
    if len(split_path) > 1:
        file_dir = split_path[0]
        file_name = split_path[1] + '.css'
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
    path = os.path.join(file_dir, file_name)
    with open(path, 'w') as file_name:
        file_name.write(content)
    return path


def get_image_path(image_url, **kwargs):
    """
    Generate Cached Image.
    """
    replace_characters = {os.sep: '_', '.': '_'}
    filter_hash_char_replace = {'#': ''}
    filter_replace = {'series(': ''}
    height = kwargs.get('height', None)
    width = kwargs.get('width', None)
    filters = kwargs.get('filters', None)

    image_url = os.path.realpath(image_url)

    save_path = multiple_replace(replace_characters, image_url)

    file_extension = image_url.split('.')[-1].lower()

    if(height):
        save_path = '_'.join([save_path, str(height)])
    if(width):
        save_path = 'x'.join([save_path, str(width)])
    if(filters):
        save_path = '_'.join([save_path, str(filters)])
    if(file_extension):
        save_path = '.'.join([save_path, file_extension])

    save_path = multiple_replace(filter_hash_char_replace, save_path)
    save_path = os.path.join(IMAGE_CACHE_DIR, save_path)

    if(not os.path.exists(save_path)):
        obj = TransformImage(image_url, height, width)
        if(not filters):
            filters = 'series()'
        if(filters.startswith("series")):
            img_obj = obj.apply_filter(filters)
        else:
            # WHY this  TODO
            filters = multiple_replace(filter_replace, filters)
            # filters = filters.rstrip(")")
            img_obj = obj.apply_filter(filters)
            # img_obj = obj._do_series(filters)
        if file_extension:
            file_extension = file_extension.upper()
            if(file_extension == 'BMP'):
                extension = file_extension
            elif(file_extension == 'PNG'):
                extension = file_extension
            elif(file_extension == 'GIF'):
                extension = file_extension
            else:
                extension = 'JPEG'
            img_obj.image.save(save_path, extension, quality=100,
                               optimize=True, progressive=True)
    return save_path

from flask import send_file
def get_css(css_file_path):
    def css_path(f):
        def decorator1(*args, **kwargs):
            path = kwargs['path']
            file_path = os.path.join(css_file_path, path)
            return send_file(file_path)
        return decorator1
    return css_path


def get_js(js_file_path):
    def js_path(f):
        def decorator2(*args, **kwargs):
            path = kwargs['path']
            file_path = os.path.join(js_file_path, path)
            return send_file(file_path)
        return decorator2
    return js_path


def get_media(media_file_path):
    def media_path(f):
        def decorator3(*args, **kwargs):
            path = kwargs['path']
            file_path = os.path.join(media_file_path, path)
            return send_file(file_path)
        return decorator3
    return media_path
