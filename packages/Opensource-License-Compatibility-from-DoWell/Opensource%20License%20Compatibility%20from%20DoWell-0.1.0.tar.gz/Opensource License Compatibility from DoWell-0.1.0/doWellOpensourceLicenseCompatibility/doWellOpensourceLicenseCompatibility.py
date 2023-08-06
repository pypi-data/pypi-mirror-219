import json

LEGALZARD_API = 'https://100080.pythonanywhere.com/api/licenses/'
import requests


class doWellOpensourceLicenseCompatibility:
    def _response(self, request):
        if request.status_code == 200:
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
        return self._response(requests.get(url=LEGALZARD_API))

    def create(self, license: dict):
        """
        Create a license by adding all the fields required
        :param license: An object with the following license parameters as listed in the main documentation.
        :return: Retrieval Object with a single license information that was created
        The response body

        :param: isSuccess: A boolean showing retrieval status
        :param data: A list with a single license.
        """
        return self._response(requests.post(url=LEGALZARD_API, data=json.dumps(license)))

    def retrieve(self, event_id: str):
        """
        Retrieve license information using an ID
        :param event_id: A string ID of the license
        :return: Retrieval Object with a single license information that was created
        The response body

        :param: isSuccess: A boolean showing retrieval status
        :param data: A list with a single license.
        """
        return self._response(requests.get(url='{}{}/'.format(LEGALZARD_API, event_id)))

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
        return self._response(requests.put(url='{}{}/'.format(LEGALZARD_API, event_id), data=json.dumps(license)))

    def delete(self, event_id: str):
        """
        Use this method to delete a license
        :param event_id: This is the eventId parameter from the license information already stored
        :return: A success object with

        :param: event_id: The license that was deleted
        :param isSuccess: Status of the action
        """
        return self._response(requests.delete(url='{}{}/'.format(LEGALZARD_API, event_id)))

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
            requests.get(url=LEGALZARD_API, params={'action_type': 'search', 'search_term': search_term}))

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
        return self._response(requests.post(url=LEGALZARD_API, data=json.dumps(comparison_data)))

    def get_compatibility_history(self, organization_id: str, user_id: str):
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
                                                    'organization_id': organization_id, 'user_id': user_id}))