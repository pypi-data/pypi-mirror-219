from __future__ import absolute_import
import os.path
from os.path import relpath
import shutil
import os
import sys
import jinja2
import typing as t

# from blendedUxLang import BlendedEnvironment
from blended.jinjaenv import BlendedEnvironment
from blendedUx.blended_flask.blended_hostlib.exceptions import BlendedException
from blendedUx.blended_flask.utils import *

env = BlendedEnvironment()

if not os.path.exists(IMAGE_CACHE_DIR):
    os.makedirs(IMAGE_CACHE_DIR)

def get_template(file_name):
    """
    """
    file_extension = file_name.split('.')[-1].lower()
    path_1 = "./templates/" + file_name
    try:
        with open(path_1, 'r', encoding='utf-8') as content_file:
                file_data = content_file.read()
                return file_data
    except Exception as e:
        if file_extension:
            print(e)
            return ''
        print(file_name)

def render_code(file_content, context):
    """
    :param file_content: compiled template content
    :param context: theme_object or context
    :return: rendered content of template.
    """
    template = env.from_string(file_content)
    
    return template.render(context)

def image(image_dict_obj, height=None, width=None, filters=None):
    """
    """
    if filters:
        if ((height == 0) or height) and ((width == 0) or width):
            pass
        elif not (height and width):
            print("Please pass height and width before using filters! error in:%s)" % image_dict_obj)
            sys.exit(0)
    elif height or width:
        filters = 'series(fill, crop(smart))'
    else:
        pass
    try:
        if height:
            float(height)
        if width:
            float(width)
    except ValueError:
        raise BlendedException("Please pass numerical value of height and width before using filters. "
                               "Default values are (0, 0)! error in:%s)" % image_dict_obj)
    try:
        relative_path = image_dict_obj.get('path')
        output = get_image_path(relative_path, height=height, width=width, filters=filters)
        url = "blended_static/media/%s" % (relpath(output, IMAGE_CACHE_DIR))
    except jinja2.exceptions.UndefinedError as exc:
        
        filename = exc.message.rsplit('attribute ')[1].replace("'", "")
        url = "blended_static/media/not_found/%s" % (filename)
    
    return url

def css(theme_object):
    """
    function to generate css file path dynamically.
    """
    # breakpoint()
    css_path = theme_object.get('meta', {}).get('css', {})
    source_path = css_path.get('compile_targets')
    rendered_require = css_path.get('render_required')
    context = {'theme': dict(theme_object)}
    try:
        try: 
            css = theme_object['css']['blendedcss']       #  code_iteration issue
        except TypeError:
            css = theme_object['css']     
                 
        file_path = os.path.join(COMPILE_DIR, 'blendedcss')
        if(rendered_require):
            css = render_code(css, context)
        try:
            path = save_css(file_path, css)
        except BlendedException as exc:
            raise BlendedException(exc)
        else:
            split_path = path.split(COMPILE_DIR)
            css_file_url = split_path[1]
            # css_file_url = "/blended_static/css/blended/blendedcss.css"
            css_file_url = "/blended_static/css/blended/%s" % (css_file_url)
            return css_file_url
    except Exception as e:
        raise(e)

from flask import url_for, get_flashed_messages

# def url_for(path, filename=""):
#     """
#     """
#     return "/%s/%s" % (path, filename)

def blended_home():
    """
    """
    default_host = '127.0.0.1'
    
    if os.environ.get("custom_host"):
        host = os.environ.get("custom_host")
    else:
        host = default_host
    if os.environ.get("custom_port"):
        try:
            port = int(os.environ.get("custom_port"))
        except:
            raise Exception("port number should be integer type!")
    else:
        port = 5000

    return "http://%s:%s"%(host,port)

def nav_links(theme, filename):
    return "%s" % (filename)


env.globals.update({'css': css,
                    'css_links': css,
                    'nav_links': nav_links,
                    'image': image,
                    "url_for": url_for,
                    'home': blended_home,
                    'get_flashed_messages': get_flashed_messages,
                    })

