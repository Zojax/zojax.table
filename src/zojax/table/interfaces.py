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
from zope import interface, schema
from zope.i18nmessageid import MessageFactory
from zope.interface.common.sequence import IFiniteSequence
from zope.contentprovider.interfaces import IContentProvider

_ = MessageFactory('zojax.table')

class ITable(IContentProvider):
    """ table, Table(context, request) """

    id = interface.Attribute('Table id')

    name = interface.Attribute('Table name')

    columns = interface.Attribute('list IColumn objects')

    headers = interface.Attribute('list IColumnHeader objects')

    footer = interface.Attribute('Table footer provider')

    dataset  = interface.Attribute('IDataset object')

    cssClass = interface.Attribute('CSS Class')

    environ = interface.Attribute('Table environment data')

    msgEmptyTable = interface.Attribute('Empty table message')

    pageSize = schema.Int(
        title = u'Page size',
        description = u'Number of elements in one page.',
        min = 0,
        default = 0,
        required = False)

    enabledColumns = schema.Tuple(
        title = u'Enabled columns',
        description = u'List of enabled columns.',
        default = (),
        required = False)

    disabledColumns = schema.Tuple(
        title = u'Disabled columns',
        description = u'List of disasbled columns.',
        default = (),
        required = False)

    def render():
        """ render table """

    def records():
        """ list of bound columns """

    def initDataset():
        """ init table dataset """

    def initColumns():
        """ init table columns """

    def initColumnHeaders():
        """ init table column headers """

    def update():
        """ update table """

    def updateContent(content, environ):
        """ update content and content environ """

    def __nonzero__():
        """ """


class IDataset(IFiniteSequence):
    """ dataset """

    def __getslice__(i, j):
        """ data slice """


class IColumn(IContentProvider):
    """ column, IColumn(context, request, table) """

    name = interface.Attribute('Column name')

    title = interface.Attribute('Column title')

    description = interface.Attribute('Column description')

    weight = interface.Attribute('Weight for sorting')

    id = interface.Attribute('CSS Id')

    cssClass = interface.Attribute('CSS Class')

    cssStyles = interface.Attribute('CSS Styles')

    table = interface.Attribute('Table')

    isAvailable = interface.Attribute('Is column available')

    # bound column
    content = interface.Attribute('Bound content')

    environ = interface.Attribute('Content environ')
    globalenviron = interface.Attribute('Content environ')

    def __bind__(content, globalenviron, environ):
        """ bind column to content object, return bound renderer """

    def query(default=None):
        """ query column value """

    def render():
        """ render column cell """


class IColumnHeader(IContentProvider):
    """ column header ColumnHeader(context, request, column) """

    id = interface.Attribute('Id')

    cssClass = interface.Attribute('CSS Class')

    column = interface.Attribute('Column')


class ITableFooter(interface.Interface):
    """ table footer """


class ITableConfiguration(interface.Interface):
    """ basic table configuration """

    pageSize = schema.Int(
        title = u'Page size',
        description = u'Number of elements in one page.',
        min = 0,
        default = 0,
        required = False)

    enabledColumns = schema.Tuple(
        title = u'Enabled columns',
        description = u'List of enabled columns.',
        default = (),
        required = False)

    disabledColumns = schema.Tuple(
        title = u'Disabled columns',
        description = u'List of disasbled columns.',
        default = (),
        required = False)


class ITableView(interface.Interface):
    """ table view """
