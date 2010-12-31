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
from zope import interface
from zope.component import getAdapters, getMultiAdapter, queryMultiAdapter

from zojax.batching.batch import Batch
from zojax.batching.session import SessionBatch

from zojax.layout.interfaces import IPagelet
from zojax.table.interfaces import ITable, ITableView
from zojax.table.interfaces import IColumn, IColumnHeader, ITableFooter
from zojax.table.interfaces import IDataset, ITableConfiguration


class Table(object):
    interface.implements(ITable)

    id = None
    name = u''
    batch = None
    cssClass = 'z-table'
    template = None
    msgEmptyTable = u'There are no items.'
    sessionBatch = False

    length = 0
    columns = ()
    headers = ()
    footer = None
    dataset = None

    pageSize = 0
    enabledColumns = ()
    disabledColumns = ()

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view
        self.environ = {}

    def initDataset(self):
        self.dataset = getMultiAdapter((self.context, self), IDataset)

    def initColumns(self):
        context = self.context
        request = self.request

        # load config
        config = queryMultiAdapter(
            (context, request, self), ITableConfiguration)
        if config is None:
            config = ITableConfiguration(self, None)

        if config is None:
            pageSize = self.pageSize
            enabledColumns = self.enabledColumns
            disabledColumns = self.disabledColumns
        else:
            pageSize = config.pageSize
            enabledColumns = config.enabledColumns
            disabledColumns = config.disabledColumns

        # generate columns
        columns = []

        if enabledColumns:
            for name in enabledColumns:
                if name not in disabledColumns:
                    column = queryMultiAdapter(
                        (context, request, self), IColumn, name)
                    if column is not None:
                        column.update()
                        if column.isAvailable:
                            columns.append(column)
        else:
            for name, column in getAdapters((context, request, self), IColumn):
                if name not in disabledColumns:
                    column.update()
                    if column.isAvailable:
                        columns.append((column.weight, column.title, column))

            columns.sort()
            columns = [column for _w,_t,column in columns]

        self.columns = columns

        if pageSize > 0:
            if self.sessionBatch:
                self.batch = SessionBatch(
                    self.dataset, size=pageSize,
                    context=context, request=request, prefix=self.name)
            else:
                self.batch = Batch(
                    self.dataset, size=pageSize,
                    context=context, request=request, prefix=self.name)

    def initColumnHeaders(self):
        context = self.context
        request = self.request

        # column headers
        headers = []
        for column in self.columns:
            header = getMultiAdapter((context, request, column), IColumnHeader)
            header.update()
            headers.append(header)

        self.headers = headers

    def update(self):
        self.initDataset()
        self.initColumns()
        self.initColumnHeaders()
        self.footer = queryMultiAdapter(
            (self, self.context, self.request), ITableFooter)
        if self.footer is not None:
            self.footer.update()

        self.length = len(self.dataset)
        self.RecordClass = RecordType(self.columns)

    def updateContent(self, content, environ):
        pass

    def render(self):
        if self.template is not None:
            return self.template()
        else:
            pagelet = queryMultiAdapter(
                (self, self.context, self.request), ITableView)
            if pagelet is not None:
                pagelet.update()
                return pagelet.render()

        raise LookupError("Can't find IPagelet for this table.")

    def records(self):
        if self.batch is not None:
            for content in self.batch:
                yield self.RecordClass(self, content)
        else:
            for content in self.dataset:
                yield self.RecordClass(self, content)

    def __nonzero__(self):
        return self.length > 0


def RecordType(columns):
    length = len(columns)
    props = {'__length__': length,
             '__columns__': columns}
    for idx in range(length):
        name = columns[idx].name
        props[name] = RecordProperty(idx)

    return type('Record', (Record,), props)


class Record(object):

    __length__ = 0
    __columns__ = ()

    def __init__(self, table, content):
        environ = {}
        table.updateContent(content, environ)

        self.__columns__ = [
            column.__bind__(content, table.environ, environ)
            for column in self.__columns__]
        self.environ = environ

    def __len__(self):
        return self.__length__

    def __iter__(self):
        return iter(self.__columns__)

    def __getitem__(self, key):
        return self.__columns__[key]


class RecordProperty(object):

    def __init__(self, idx):
        self.__idx = idx

    def __get__(self, inst, klass):
        return inst.__columns__[self.__idx]
