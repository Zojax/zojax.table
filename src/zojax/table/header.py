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
from interfaces import IColumn, IColumnHeader


class ColumnHeader(object):
    interface.implements(IColumnHeader)
    component.adapts(interface.Interface, interface.Interface, IColumn)

    id = None
    cssClass = None

    def __init__(self, context, request, column):
        self.context = context
        self.request = request
        self.column = column

    def update(self):
        pass

    def render(self):
        return self.column.title

    @property
    def cssClass(self):
        return self.column.cssClass
