
import logging
import os
import subprocess
import sys
from collections import defaultdict
from operator import itemgetter

logging.basicConfig(level=logging.DEBUG)


class GenerateHierarchy:
    def __init__(self):
        # it will have a module:class:children mapping.
        self.class_dict = defaultdict(lambda: defaultdict(list))

    def show_class(self, name, class_data):
        """show the class and its contents.

        Arguments:
            name {str} -- name of the class for which data is to be shown.
            class_data {list} -- complete class_data as generated from pyclbr.
        """
        # logging.debug(class_data)
        self.class_dict[name] = []
        self.show_super_classes(name, class_data)

    def show_methods(self, class_name, class_data):
        """generates all the methods in a given class

        Arguments:
            class_name {str} -- name of the class whose methods are to be shown.
            class_data {list} -- complete class_data as generated from pyclbr.

        Returns:
            list -- all the methods that are declared in the given class(name param)
        """
        methods = []
        for name, _ in sorted(class_data.methods.items(), key=itemgetter(1)):
            # logging.debug('  Method: {0} [{1}]'.format(name, lineno))
            methods.append(name)
        return methods

    def show_super_classes(self, name, class_data, object):
        """Shows super classes for a given class

        Arguments:
            name {str} -- name of the class for which superclasses are to be collected
            class_data {#TODO} -- complete class_data as generated from pyclbr.

        Returns:
            list -- names of superclasses
        """
        super_class_names = []
        for super_class in class_data.super:
            if super_class == 'object':
                continue
            if isinstance(super_class, str):
                # find the class in covered modules
                found = False
                for module in object.class_object_mapping.keys():
                    for class_ in object.class_object_mapping[module].keys():
                        if object.class_object_mapping[module][class_].name == super_class:
                            found = True
                            super_class = object.class_object_mapping[module][class_]
                            break
                    if found:
                        break
            super_class_names.append(
                {
                    'parent_module': super_class.module,
                    'parent_class': super_class.name
                }
            )
        for super_class_name in super_class_names:
            if self.class_dict.get(super_class_name['parent_module']):
                if self.class_dict.get(super_class_name['parent_class']):
                    self.class_dict[super_class_name['parent_module']][super_class_name['parent_class']].append(
                        {
                            'child_module': class_data.module,
                            'child_class': name
                        }
                    )
            else:
                self.class_dict[super_class_name['parent_module']][super_class_name['parent_class']] = [
                    {
                        'child_module': class_data.module,
                        'child_class': name
                    }
                ]
        # adding all parents for a class in one place for later usage: children
        return super_class_names

    def get_children(self, name, class_data):
        """returns all the computed children for a given class if any
        otherwise returns an empty list.

        Arguments:
            name {[type]} -- [description]

        Returns:
            list -- list of classes that are children for a given class.
        """
        module = class_data.module
        if self.class_dict.get(module, None):
            if self.class_dict[module].get(name):
                return self.class_dict[class_data.module][name]
        return []
