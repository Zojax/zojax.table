##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface, component
from zope.i18n import translate

from interfaces import IColumn, _


class Column(object):
    interface.implements(IColumn)

    name = u''
    title = u''
    description = u''
    id = None
    cssClass = None
    cssStyles = None
    weight = 0
    isAvailable = True

    content = None
    environ = None
    globalenviron = None

    template = None

    def __init__(self, context, request, table):
        self.context = context
        self.request = request
        self.table = table

    def query(self, default=None):
        raise NotImplemented('query')

    def __bind__(self, content, globalenviron, environ):
        clone = self.__class__.__new__(self.__class__)
        clone.__dict__.update(self.__dict__)
        clone.content = content
        clone.environ = environ
        clone.globalenviron = globalenviron
        return clone

    def update(self):
        pass

    def render(self):
        if self.template is not None:
            return self.template()
        else:
            return translate(self.query(), context=self.request)


class DisabledColumn(Column):

    isAvailable = False


class AttributeColumn(Column):

    attrName = ''

    def query(self, default=None):
        return getattr(self.content, self.attrName, default)


class BoolColumn(AttributeColumn):

    def render(self):
        if not self.query():
            return _(u'No')
        return _(u'Yes')
