import json

LEGALZARD_API = 'https://100080.pythonanywhere.com/api/public/licenses/'
import requests
from requests.structures import CaseInsensitiveDict


class doWellOpensourceLicenseCompatibility:
    headers = CaseInsensitiveDict()

    def __init__(self, api_key):
        self.headers['API-KEY'] = api_key

    def _response(self, request):
        if request.status_code in [200, 201]:
            return request.json()
        return json.dumps({'Error': '{} {}'.format(request.status_code, request.content.decode('utf-8'))})

    def get_all(self):
        """
        Get all licenses submitted
        :return: An Object with retrieval status and an list of all licenses

        The response body

        :param: isSuccess: A boolean showing retrieval status
        :param data: A list of licenses.

        """
        return self._response(requests.get(url=LEGALZARD_API, headers=self.headers))

    def create(self, license: dict):
        """
        Create a license by adding all the fields required
        :param license: An object with the following license parameters as listed in the main documentation.
        :return: Retrieval Object with a single license information that was created
        The response body

        :param: isSuccess: A boolean showing retrieval status
        :param data: A list with a single license.
        """
        return self._response(requests.post(url=LEGALZARD_API, json=json.dumps(license), headers=self.headers))

    def retrieve(self, event_id: str):
        """
        Retrieve license information using an ID
        :param event_id: A string ID of the license
        :return: Retrieval Object with a single license information that was created
        The response body

        :param: isSuccess: A boolean showing retrieval status
        :param data: A list with a single license.
        """
        return self._response(requests.get(url='{}{}/'.format(LEGALZARD_API, event_id), headers=self.headers))

    def update(self, event_id: str, license: dict):
        """
        This method updates the license information stored on the database
        :param event_id: This is the eventId parameter from the license information already stored
        :param license: An object with the following license parameters as listed in the main documentation.
        :return: New updated license information

        The response body

        :param: isSuccess: A boolean showing retrieval status
        :param data: A list with a single license.
        """
        return self._response(
            requests.put(url='{}{}/'.format(LEGALZARD_API, event_id), json=json.dumps(license), headers=self.headers))

    def delete(self, event_id: str):
        """
        Use this method to delete a license
        :param event_id: This is the eventId parameter from the license information already stored
        :return: A success object with

        :param: event_id: The license that was deleted
        :param isSuccess: Status of the action
        """
        return self._response(requests.delete(url='{}{}/'.format(LEGALZARD_API, event_id), headers=self.headers))

    def search(self, search_term: str):
        """
        Use this method to search for licenses containing some phrase
        :param search_term: This is the search phrase used to filter the licenses
        :return: Licenses matching the search parameters
        The response body

        :param: isSuccess: A boolean showing retrieval status
        :param data: A list with matching licenses.
        """
        return self._response(
            requests.get(url=LEGALZARD_API, params={'action_type': 'search', 'search_term': search_term},
                         headers=self.headers))

    def check_compatibility(self, comparison_data: dict):
        """
        This method allows you to check license compatibility of two licenses
        :param comparison_data: An object with the comparison fields
        :return: Comparison results

        The request object comparison_data

        :param license_event_id_one: License 1 event_id
        :param license_event_id_two: License 2 event_id
        :param user_id: Your user Id
        :param organization_id: Your Organization Id

        The response body

        :param is_compatible: Status of compatibility
        :param percentage_of_compatibility: Percentage of compatibility
        :param license_1_event_id: License 1 event_id
        :param license_2_event_id: License 2 event_id
        :param identifier: Comparison Id
        :param license_1: License object for license 1
        :param license_2: License object for license 2

        """
        comparison_data['action_type'] = 'check-compatibility'
        return self._response(requests.post(url=LEGALZARD_API, json=json.dumps(comparison_data), headers=self.headers))

    def get_compatibility_history(self, organization_id: str = None, user_id: str = None):
        """
        Get Compatibility Check History by a user.
        :param organization_id: Your Organization Id
        :param user_id: Your User Id
        :return: A Comparison History Object

        The Response body

        :param isSuccess: Request status
        :param data: a list of License comparison history objects
        """
        return self._response(
            requests.get(url=LEGALZARD_API, params={'collection_type': 'license-compatibility-history',
                                                    'organization_id': organization_id, 'user_id': user_id},
                         headers=self.headers))