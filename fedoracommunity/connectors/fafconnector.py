# This file is part of Fedora Community.
# Copyright (C) 2008-2010  Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import koji

from datetime import datetime

import requests

from tg import config
from cgi import escape
from paste.httpexceptions import HTTPBadRequest
from paste.httpexceptions import HTTPBadGateway


from fedoracommunity.connectors.api import \
    IConnector, IQuery, ParamFilter
from fedoracommunity.connectors.api import get_connector
from moksha.common.lib.dates import DateTimeDisplay


class FafConnector(IConnector, IQuery):
    _method_paths = {}
    _query_paths = {}
    _cache_prompts = {}

    def __init__(self, environ=None, request=None):
        super(FafConnector, self).__init__(environ, request)

    @classmethod
    def query_problems_cache_prompt(cls, msg):
        '''
        if not '.buildsys.build.state.change' in msg['topic']:
            return

        if msg['msg']['instance'] != 'primary':
            return

        # Kill two cache slots.  one for builds of this package in any state
        # and one for builds of this package in this particular state.
        name = msg['msg']['name']
        return [
            {'package': name, 'state': ''}, # '' means 'all'
            {'package': name, 'state': msg['msg']['new']},
        ]
        '''
        pass

    # IConnector
    @classmethod
    def register(cls):
        cls.register_query_problems()

    #IQuery
    @classmethod
    def register_query_problems(cls):
        path = cls.register_query(
            'query_problems',
            cls.query_problems,
            cls.query_problems_cache_prompt,
            primary_key_col='id',
            default_sort_col='count',
            default_sort_order=-1,
            can_paginate=True)

        path.register_column(
            'id',
            default_visible=True,
            can_sort=True,
            can_filter_wildcards=False)

        path.register_column(
            'status',
            default_visible=True,
            can_sort=True,
            can_filter_wildcards=False)

        path.register_column(
            'crash_function',
            default_visible=True,
            can_sort=True,
            can_filter_wildcards=True)

        path.register_column(
            'count',
            default_visible=True,
            can_sort=True,
            can_filter_wildcards=False)

        f = ParamFilter()
        f.add_filter('package', ['p'], allow_none=True)
        f.add_filter('status', ['s'], allow_none=True)
        f.add_filter('crash_function', allow_none=True, cast=bool)
        cls._query_builds_filter = f

    def query_problems(self, start_row=None,
                     rows_per_page=10,
                     order=-1,
                     sort_col=None,
                     filters=None,
                     **params):

        if not filters:
            filters = {}
        filters = self._query_builds_filter.filter(filters, conn=self)

        package = filters.get('package', '')
        status = filters.get('status')
        crash_function = filters.get('crash_function')

        url = "https://retrace.fedoraproject.org/faf/problems/?component_names=" + package
        headers = {'Accept': 'application/json'}
        r = requests.get(url, headers=headers)
        # TODO try catch

        # get problems from response
        problems = r.json()['problems']

        return (len(problems), problems)
