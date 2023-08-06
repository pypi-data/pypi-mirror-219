from .annotation import Annotation

import pkg_resources
import os

def load_js():
    resource_package = __name__
    resource_path = os.path.join('js', 'vulcan_annotation.js')
    return pkg_resources.resource_string(resource_package, resource_path).decode()


def load_va_dom():
    resource_package = __name__
    resource_path = os.path.join('js', 'va_dom.js')
    return pkg_resources.resource_string(resource_package, resource_path).decode()
