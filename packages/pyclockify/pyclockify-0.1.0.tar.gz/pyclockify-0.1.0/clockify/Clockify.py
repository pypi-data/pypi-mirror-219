import requests
from attr import define, field


@define
class Clockify:
    api_key: str
    base_url: str = field(default="https://api.clockify.me/api/v1")

    def _make_request(self, method, endpoint, params=None, data=None):
        headers = {
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key
        }
        url = f"{self.base_url}/{endpoint}"

        response = requests.request(method, url, headers=headers, params=params, json=data)
        response.raise_for_status()

        return response.json()

    def get_workspace(self, workspace_id):
        return next((workspace for workspace in self.get_workspaces() if workspace['id'] == workspace_id), None)

    def get_workspace_by_name(self, workspace_name):
        return next((workspace for workspace in self.get_workspaces() if workspace['name'] == workspace_name), None)

    def get_workspaces(self):
        return self._make_request("GET", "workspaces")

    def get_users(self, workspace_id):
        endpoint = f"workspaces/{workspace_id}/users"
        return self._make_request("GET", endpoint)

    def get_user(self, workspace_id, user_id):
        endpoint = f"workspaces/{workspace_id}/users/{user_id}"
        return self._make_request("GET", endpoint)

    def get_projects(self, workspace_id):
        endpoint = f"workspaces/{workspace_id}/projects"
        return self._make_request("GET", endpoint)

    def get_clients(self, workspace_id):
        endpoint = f"workspaces/{workspace_id}/clients"
        return self._make_request("GET", endpoint)

    def get_tags(self, workspace_id):
        endpoint = f"workspaces/{workspace_id}/tags"
        return self._make_request("GET", endpoint)

    def get_time_entries_by_user(self, workspace_id, user_id):
        endpoint = f"workspaces/{workspace_id}/user/{user_id}/time-entries"
        return self._make_request("GET", endpoint)

    def get_time_entries(self, workspace_id):
        users = self.get_users(workspace_id)
        return [entry for user in users for entry in self.get_time_entries_by_user(workspace_id, user['id'])]

    def get_time_entries_by_username(self, workspace_id):
        users = self.get_users(workspace_id)
        return {user['name']: self.get_time_entries_by_user(workspace_id, user['id']) for user in users}

    # Agrega más métodos GET según tus necesidades para interactuar con otros recursos de la API


# Ejemplo de uso
if __name__ == "__main__":
    clockify_api = Clockify("OGViNzFhMjMtOWVkZS00NWU2LWE2ZjUtYmU4ZmM1MThkYzUy")
    workspaces = clockify_api.get_workspaces()
    print("Workspaces:")
    print(workspaces)

    if workspaces:
        workspace_id = workspaces[1]['id']
        workspace = clockify_api.get_workspace(workspace_id)
        print("\nWorkspace:")
        print(workspace)

        projects = clockify_api.get_projects(workspace_id)
        print("\nProjects:")
        print(projects)

        clients = clockify_api.get_clients(workspace_id)
        print("\nClients:")
        print(clients)

        tags = clockify_api.get_tags(workspace_id)
        print("\nTags:")
        print(tags)

        time_entries = clockify_api.get_time_entries(workspace_id)
        print("\nTime Entries:")
        print(time_entries)

        time_entries_by_username = clockify_api.get_time_entries_by_username(workspace_id)
        print("\nTime Entries by Username:")
        print(time_entries_by_username)
