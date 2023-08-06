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

from osc_lib.command import command
from osc_lib import utils as oscutils

from esileapclient.v1.event import Event as EVENT_RESOURCE

LOG = logging.getLogger(__name__)


class ListEvent(command.Lister):
    """List events."""

    log = logging.getLogger(__name__ + ".ListEvent")

    def get_parser(self, prog_name):
        parser = super(ListEvent, self).get_parser(prog_name)

        parser.add_argument(
            '--project',
            dest='project_id',
            required=False,
            help="Show all events associated with given project ID or name.")
        parser.add_argument(
            '--last-event-id',
            dest='last_event_id',
            required=False,
            help="Show events after this event ID.")
        parser.add_argument(
            '--last-notification-time',
            dest='last_event_time',
            required=False,
            help="Show events after this notification time.")
        parser.add_argument(
            '--event-type',
            dest='event_type',
            required=False,
            help="Show events matching this event type.")
        parser.add_argument(
            '--resource-type',
            dest='resource_type',
            required=False,
            help="Show events matching this resource type.")
        parser.add_argument(
            '--resource-uuid',
            dest='resource_uuid',
            required=False,
            help="Show events matching this resource ID or name.")

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.lease

        filters = {
            'lessee_or_owner_id': parsed_args.project_id,
            'last_event_id': parsed_args.last_event_id,
            'last_event_time': parsed_args.last_event_time,
            'event_type': parsed_args.event_type,
            'resource_type': parsed_args.resource_type,
            'resource_uuid': parsed_args.resource_uuid,
        }

        data = client.event.list(filters)
        columns = EVENT_RESOURCE.fields.keys()
        labels = EVENT_RESOURCE.fields.values()

        return (labels,
                (oscutils.get_item_properties(s, columns) for s in data))
