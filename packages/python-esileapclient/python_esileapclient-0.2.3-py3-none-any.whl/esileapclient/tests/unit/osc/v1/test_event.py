import copy

from esileapclient.osc.v1 import event
from esileapclient.tests.unit.osc.v1 import base
from esileapclient.tests.unit.osc.v1 import fakes


class TestEvent(base.TestESILeapCommand):

    def setUp(self):
        super(TestEvent, self).setUp()

        self.client_mock = self.app.client_manager.lease
        self.client_mock.reset_mock()


class TestEventList(TestEvent):

    def setUp(self):
        super(TestEventList, self).setUp()

        self.client_mock.event.list.return_value = [
            base.FakeResource(copy.deepcopy(fakes.EVENT))
        ]
        self.cmd = event.ListEvent(self.app, None)

    def test_event_list(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        filters = {
            'lessee_or_owner_id': parsed_args.project_id,
            'last_event_id': parsed_args.last_event_id,
            'last_event_time': parsed_args.last_event_time,
            'event_type': parsed_args.event_type,
            'resource_type': parsed_args.resource_type,
            'resource_uuid': parsed_args.resource_uuid,
        }

        self.client_mock.event.list.assert_called_with(filters)

        collist = [
            "ID",
            "Event Type",
            "Event Time",
            "Object Type",
            "Object UUID",
            "Resource Type",
            "Resource UUID",
            "Lessee ID",
            "Owner ID",
        ]

        self.assertEqual(collist, list(columns))

        datalist = ((fakes.event_id,
                     fakes.event_type,
                     fakes.event_time,
                     fakes.object_type,
                     fakes.lease_uuid,
                     fakes.lease_resource_type,
                     fakes.lease_resource_uuid,
                     fakes.lease_project_id,
                     fakes.lease_owner_id,
                     ),)
        self.assertEqual(datalist, tuple(data))
