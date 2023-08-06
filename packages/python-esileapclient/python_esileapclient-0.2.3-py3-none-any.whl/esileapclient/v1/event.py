#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from esileapclient.common import base

LOG = logging.getLogger(__name__)


class Event(base.Resource):

    detailed_fields = {
        'id': "ID",
        'event_type': "Event Type",
        'event_time': "Event Time",
        'object_type': "Object Type",
        'object_uuid': "Object UUID",
        'resource_type': "Resource Type",
        'resource_uuid': "Resource UUID",
        'lessee_id': "Lessee ID",
        'owner_id': "Owner ID",
    }

    fields = {
        'id': "ID",
        'event_type': "Event Type",
        'event_time': "Event Time",
        'object_type': "Object Type",
        'object_uuid': "Object UUID",
        'resource_type': "Resource Type",
        'resource_uuid': "Resource UUID",
        'lessee_id': "Lessee ID",
        'owner_id': "Owner ID",
    }

    _creation_attributes = ['id', 'event_type', 'event_time',
                            'object_type', 'object_uuid',
                            'resource_type', 'resource_uuid',
                            'lessee_id', 'owner_id']

    def __repr__(self):
        return "<Event %s>" % self._info


class EventManager(base.Manager):
    resource_class = Event
    _resource_name = 'events'

    def list(self, filters, os_esileap_api_version=None):
        """Retrieve a list of events.
        :returns: A list of events.
        """

        resource_id = ''

        url_variables = EventManager._url_variables(filters)
        url = self._path(resource_id) + url_variables

        events = self._list(url,
                            os_esileap_api_version=os_esileap_api_version)

        if type(events) is list:
            return events
