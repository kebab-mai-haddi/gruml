
import logging
import os
import subprocess
import sys
from operator import itemgetter

logging.basicConfig(level=logging.DEBUG)


class GenerateHierarchy:
    def __init__(self):
        self.class_dict = {}  # it will have a class:children mapping.

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
        for name, _ in sorted(class_data.methods.items(),
                              key=itemgetter(1)):
            # logging.debug('  Method: {0} [{1}]'.format(name, lineno))
            methods.append(name)
        return methods

    def show_super_classes(self, name, class_data):
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
                super_class_names.append(super_class)
            else:
                super_class_names.append(super_class.name)
        for super_class_name in super_class_names:
            if self.class_dict.get(super_class_name, None):
                self.class_dict[super_class_name].append(name)
            else:
                self.class_dict[super_class_name] = [name]
        # adding all parents for a class in one place for later usage: children
        return super_class_names

    def get_children(self, name):
        """returns all the computed children for a given class if any
        otherwise returns an empty list.

        Arguments:
            name {[type]} -- [description]

        Returns:
            list -- list of classes that are children for a given class.
        """
        if self.class_dict.get(name, None):
            return self.class_dict[name]
        return []
