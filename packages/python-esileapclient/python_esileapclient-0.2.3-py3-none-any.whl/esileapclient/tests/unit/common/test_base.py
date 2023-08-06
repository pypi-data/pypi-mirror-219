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

import testtools
import copy
from unittest import mock

from esileapclient.common import base


FAKE_RESOURCE = {
    'uuid': '11111111-2222-3333-4444-555555555555',
    'attribute1': '1',
    'attribute2': '2',
}
FAKE_RESOURCE_2 = {
    'uuid': '66666666-7777-8888-9999-000000000000',
    'attribute1': '3',
    'attribute2': '4',
}


CREATE_FAKE_RESOURCE = copy.deepcopy(FAKE_RESOURCE)
del CREATE_FAKE_RESOURCE['uuid']

INVALID_ATTRIBUTE_FAKE_RESOURCE = {
    'non-existent-attribute': 'bad',
    'attribute1': '1',
    'attribute2': '2',
}


class FakeResponse(object):
    def __init__(self, headers=None, body=None, status=None,
                 request_headers={}):
        """Fake object to help testing.
        :param headers: dict representing HTTP response headers
        :param body: file-like object
        """
        self.headers = headers
        self.body = body
        self.status_code = status
        self.request = mock.Mock()
        self.request.headers = request_headers


VALID_CREATE_RESPONSE = FakeResponse(status=201)
VALID_RESPONSE = FakeResponse(status=200)


class FakeResource(base.Resource):

    fields = {
        'uuid': 'UUID',
        'attribute1': 'Attribute 1',
        'attribute2': 'Attribute 2',
    }

    detailed_fields = {
        'uuid': 'UUID',
        'attribute1': 'Attribute 1',
        'attribute2': 'Attribute 2',
        'attribute3': 'Attribute 3',
    }

    _creation_attributes = ['attribute1', 'attribute2']

    def __repr__(self):
        return "<FakeResource %s>" % self._info


class FakeResourceManager(base.Manager):
    resource_class = FakeResource
    _resource_name = 'fakeresources'


class ManagerTestCase(testtools.TestCase):

    def test__create(self):

        manager = FakeResourceManager(None)
        with mock.patch.object(manager, 'api') as mock_api:

            mock_api.json_request.return_value = (
                VALID_CREATE_RESPONSE,
                FAKE_RESOURCE)

            resource = manager._create(**CREATE_FAKE_RESOURCE)

            mock_api.json_request.assert_called_once_with(
                'POST', '/v1/fakeresources',
                **{'body': CREATE_FAKE_RESOURCE})

            self.assertIsInstance(resource, FakeResource)
            self.assertEqual(resource._info, FAKE_RESOURCE)

    def test__create_microversion_override(self):

        manager = FakeResourceManager(None)
        with mock.patch.object(manager, 'api') as mock_api:

            mock_api.json_request.return_value = (
                VALID_CREATE_RESPONSE,
                FAKE_RESOURCE)

            resource = manager._create(os_esileap_api_version='1.10',
                                       **CREATE_FAKE_RESOURCE)

            mock_api.json_request.assert_called_once_with(
                'POST', '/v1/fakeresources',
                **{'body': CREATE_FAKE_RESOURCE,
                   'headers': {'X-OpenStack-ESI-Leap-API-Version': '1.10'}})

            self.assertIsInstance(resource, FakeResource)
            self.assertEqual(resource._info, FAKE_RESOURCE)

    def test__create_with_invalid_attribute(self):

        manager = FakeResourceManager(None)
        with mock.patch.object(manager, 'api'):

            self.assertRaises(
                Exception,
                manager._create,
                **INVALID_ATTRIBUTE_FAKE_RESOURCE)

    def test__list(self):

        manager = FakeResourceManager(None)
        with mock.patch.object(manager, 'api') as mock_api:

            mock_api.json_request.return_value = (
                VALID_RESPONSE,
                {'fakeresources': [FAKE_RESOURCE, FAKE_RESOURCE_2]})

            resources_list = manager._list(manager._path())

            mock_api.json_request.assert_called_once_with(
                'GET', '/v1/fakeresources')

            expected_resources = [FakeResource(None, FAKE_RESOURCE),
                                  FakeResource(None, FAKE_RESOURCE_2)]

            self.assertIsInstance(resources_list, list)
            assert (len(expected_resources) == 2)

            self.assertIsInstance(resources_list[0], FakeResource)

            self.assertEqual(resources_list[0]._info,
                             expected_resources[0]._info)
            self.assertEqual(resources_list[1]._info,
                             expected_resources[1]._info)

    def test__list_microversion_override(self):

        manager = FakeResourceManager(None)
        with mock.patch.object(manager, 'api') as mock_api:

            mock_api.json_request.return_value = (
                VALID_RESPONSE,
                {'fakeresources': [FAKE_RESOURCE, FAKE_RESOURCE_2]})

            resources_list = manager._list(manager._path(),
                                           os_esileap_api_version='1.10')

            mock_api.json_request.assert_called_once_with(
                'GET', '/v1/fakeresources',
                **{'headers': {'X-OpenStack-ESI-Leap-API-Version': '1.10'}})

            expected_resources = [FakeResource(None, FAKE_RESOURCE),
                                  FakeResource(None, FAKE_RESOURCE_2)]

            self.assertIsInstance(resources_list, list)
            assert (len(expected_resources) == 2)

            self.assertIsInstance(resources_list[0], FakeResource)

            self.assertEqual(resources_list[0]._info,
                             expected_resources[0]._info)
            self.assertEqual(resources_list[1]._info,
                             expected_resources[1]._info)

    def test__get(self):

        manager = FakeResourceManager(None)
        with mock.patch.object(manager, 'api') as mock_api:

            mock_api.json_request.return_value = (
                VALID_RESPONSE,
                FAKE_RESOURCE)

            resource = manager._get(FAKE_RESOURCE['uuid'])

            mock_api.json_request.assert_called_once_with(
                'GET', '/v1/fakeresources/%s' % FAKE_RESOURCE['uuid'],)

            self.assertIsInstance(resource, FakeResource)
            self.assertEqual(FAKE_RESOURCE, resource._info)

    def test__get_microversion_override(self):

        manager = FakeResourceManager(None)
        with mock.patch.object(manager, 'api') as mock_api:

            mock_api.json_request.return_value = (
                VALID_RESPONSE,
                FAKE_RESOURCE)

            resource = manager._get(FAKE_RESOURCE['uuid'],
                                    os_esileap_api_version='1.10')

            mock_api.json_request.assert_called_once_with(
                'GET', '/v1/fakeresources/%s' % FAKE_RESOURCE['uuid'],
                **{'headers': {'X-OpenStack-ESI-Leap-API-Version': '1.10'}})

            self.assertIsInstance(resource, FakeResource)
            self.assertEqual(FAKE_RESOURCE, resource._info)

    def test__get_invalid_resource_id_raises(self):

        manager = FakeResourceManager(None)
        with mock.patch.object(manager, 'api'):
            resource_ids = [[], {}, False, '', 0, None, (), 'hi']
            for resource_id in resource_ids:
                self.assertRaises(Exception, manager._get,
                                  resource_id=resource_id)

    def test__delete(self):

        manager = FakeResourceManager(None)
        with mock.patch.object(manager, 'api') as mock_api:

            mock_api.json_request.return_value = (
                VALID_RESPONSE,
                None)

            resp = manager._delete(
                resource_id=FAKE_RESOURCE['uuid'])

            mock_api.json_request.assert_called_once_with(
                'DELETE',
                '/v1/fakeresources/%s' % FAKE_RESOURCE['uuid'])

            self.assertEqual(resp, None)

    def test__delete_microversion_override(self):

        manager = FakeResourceManager(None)
        with mock.patch.object(manager, 'api') as mock_api:

            mock_api.json_request.return_value = (
                VALID_RESPONSE,
                None)

            resp = manager._delete(
                resource_id=FAKE_RESOURCE['uuid'],
                os_esileap_api_version='1.10')

            mock_api.json_request.assert_called_once_with(
                'DELETE',
                '/v1/fakeresources/%s' % FAKE_RESOURCE['uuid'],
                **{'headers': {'X-OpenStack-ESI-Leap-API-Version': '1.10'}})

            self.assertEqual(resp, None)

    def test__delete_invalid_resource_id_raises(self):

        manager = FakeResourceManager(None)
        with mock.patch.object(manager, 'api'):
            resource_ids = [[], {}, False, '', 0, None, (), 'hi']
            for resource_id in resource_ids:
                self.assertRaises(Exception, manager._delete,
                                  resource_id=resource_id)
