# -*- coding: utf-8 -*-
"""
Component registry

based on zope.interfaces

"""

from __future__ import absolute_import, print_function, unicode_literals

import importlib

from zope.interface import interface, declarations, implementedBy
from zope.interface.adapter import AdapterRegistry

from .interfaces import ICaliop

_iface_registry = AdapterRegistry()


def configure(config):
    for iface in ['data', 'index']:
        for key, val in config.get('interfaces.storage.%s' % iface).items():
            mod, impl = val.rsplit('.', 1)
            register(getattr(importlib.import_module(mod), impl))


def register(registred_type, *adapted_ifaces, **kwargs):
    """ Register an adapter class for an original interface that implement
    adapted_ifaces. """
    assert registred_type, 'You need to pass an Interface'
    original_iface = kwargs.get('adapt', ICaliop)

    # deal with class->interface adapters:
    if not isinstance(original_iface, interface.InterfaceClass):
        original_iface = declarations.implementedBy(original_iface)

    if not adapted_ifaces:
        adapted_ifaces = implementedBy(registred_type)

    for iface in adapted_ifaces:
        factory = _iface_registry.registered([original_iface], iface)
        if factory is not None:
            raise ValueError('an adapter (%s) was already registered.' %
                             (factory, ))

    for iface in adapted_ifaces:
        _iface_registry.register([original_iface], iface, '', registred_type)


def get(adapted_iface, original_iface=ICaliop):
    """ Return registered adapter for a given class and interface. """

    if not isinstance(original_iface, interface.InterfaceClass):
        if hasattr(original_iface, '__class__'):
            original_iface = original_iface.__class__
        original_iface = declarations.implementedBy(original_iface)

    registred_type = _iface_registry.lookup1(original_iface, adapted_iface, '')
    if not registred_type:
        raise NotImplementedError('No implementation has been registered')
    return registred_type


_instances = {}

def get_component(adapted_iface, original_iface=ICaliop):
    """ Return a singleton object for the given interface """

    if (adapted_iface, original_iface) not in _instances:
        _instances[(adapted_iface, original_iface)] = get(adapted_iface,
                                                          original_iface)()

    return _instances[(adapted_iface, original_iface)]
