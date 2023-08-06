from requests import get, post, put, delete
from json import JSONDecodeError
from tqdm import tqdm
from time import sleep
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file


class ClickUpAPI:
    """This class represents an API client for the ClickUp API."""

    def __init__(self, api_key: str) -> None:
        """Initializes the API client with the provided API key.

        Args:
            api_key (str): The API key for the ClickUp account.
        """
        self.headers = {"Authorization": api_key}

    def get_all_folders(self, space_id: str) -> dict:
        """Get all folders for a space.

        Args:
            space_id (str): The ID of the space to get folders for.

        Returns:
            dict: A dictionary containing information about all folders for the space.
        """
        url = f"https://api.clickup.com/api/v2/space/{space_id}/folder"
        response = None
        while response is None:
            try:
                response = get(url, headers=self.headers)
            except:
                # Handle connection error, and try again in 1 second
                pass
            sleep(1)
        return response.json()

    def set_new_folder(self, space_id: str, folder_name: str) -> dict:
        """Create a new folder in a space.

        Args:
            space_id (str): The ID of the space to create the folder in.
            folder_name (str): The name of the new folder.

        Returns:
            dict: A dictionary containing information about the new folder.
        """
        url = f"https://api.clickup.com/api/v2/space/{space_id}/folder"
        payload = {"name": folder_name}
        response = None
        while response is None:
            try:
                response = post(url, headers=self.headers, json=payload)
            except:
                # Handle connection error, and try again in 1 second
                pass
            sleep(1)
        return response.json()

    def set_new_list(self, folder_id: str, list_name: str) -> dict:
        """Create a new list in a folder.

        Args:
            folder_id (str): The ID of the folder to create the list in.
            list_name (str): The name of the new list.

        Returns:
            dict: A dictionary containing information about the new list.
        """
        url = f"https://api.clickup.com/api/v2/folder/{folder_id}/list"
        payload = {"name": list_name}
        response = None
        while response is None:
            try:
                response = post(url, headers=self.headers, json=payload)
            except:
                # Handle connection error, and try again in 1 second
                pass
            sleep(1)
        return response.json()

    def get_all_spaces(self, team_id: str) -> dict:
        """Get all spaces for a team.

        Args:
            team_id (str): The ID of the team to get spaces for.

        Returns:
            dict: A dictionary containing information about all spaces for the team.
        """
        url = f"https://api.clickup.com/api/v2/team/{team_id}/space"
        response = None
        while response is None:
            try:
                response = get(url, headers=self.headers)
            except:
                # Handle connection error, and try again in 1 second
                pass
            sleep(1)
        return response.json()

    def get_all_tags(self, space_id: str) -> dict:
        """Retrieves all tags for a given space ID.

        Args:
            space_id (str): The ID of the space to retrieve tags from.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        url = f"https://api.clickup.com/api/v2/space/{space_id}/tag"
        response = None
        while response is None:
            try:
                response = get(url, headers=self.headers)
            except:
                # Handle connection error, and try again in 1 second
                pass
            sleep(1)
        return response.json()

    def get_task(self, task_id: str) -> dict:
        """Retrieves a task for a given task ID.

        Args:
            task_id (str): The ID of the task to retrieve.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        url = f"https://api.clickup.com/api/v2/task/{task_id}"
        response = None
        while response is None:
            try:
                response = get(url, headers=self.headers)
            except:
                # Handle connection error, and try again in 1 second
                pass
            sleep(1)
        try:
            return response.json()
        except JSONDecodeError as e:
            # Log the error and return an empty dictionary
            print(f"Task URL: {url}. Error decoding JSON response: {e}")
            return {}

    def get_all_tasks(
        self,
        list_id: str,
        archived: bool = False,
        include_closed: bool = False,
    ) -> dict:
        """Retrieves a list of tasks for a given list ID.

        Args:
            list_id (str): The ID of the list to retrieve tasks from.
            archived (bool, optional): Whether to include archived tasks in the response. Defaults to False.
            include_closed (bool, optional): Whether to include closed tasks in the response. Defaults to False.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        all_tasks = []
        page = 0
        url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
        while True:
            tqdm.write(f"Downloading page {page}")
            query = {
                "archived": str(archived).lower(),
                "page": str(page),
                "include_closed": str(include_closed).lower(),
            }
            response = None
            while response is None:
                try:
                    response = get(url, headers=self.headers, params=query)
                except:
                    # Handle connection error, and try again in 1 second
                    pass
                sleep(1)
            data = response.json()

            if data["tasks"] == []:
                break
            all_tasks.extend(data["tasks"])
            page += 1
        return dict(tasks=all_tasks)

    def delete_all_tasks(self, list_id: str) -> dict:
        """Deletes all tasks from the specified list.

        Args:
            list_id (str): The ID of the list to delete tasks from.

        Returns:
            dict: A dictionary containing the IDs of all the deleted tasks.
        """
        tasks = self.get_all_tasks(list_id=list_id, include_closed=True)
        all_tasks = []
        for task in tqdm(tasks["tasks"], desc=f"Deleting tasks from list {list_id}"):
            task_id = task["id"]
            url = f"https://api.clickup.com/api/v2/task/{task_id}"
            response = None
            while response is None:
                try:
                    response = delete(url, headers=self.headers)
                    all_tasks.extend(task_id)
                except:
                    # Handle connection error, and try again in 1 second
                    pass
                sleep(1)
        return dict(tasks=all_tasks)

    def set_new_task(
        self,
        list_id: str,
        name: str,
        description: str,
        custom_task_ids: bool = True,
        team_id: str = "123",
        tags: list = [],
        status: str = "to do",
        parent: str | None = None,
    ):
        """Creates a new task in a given list.

        Args:
            list_id (str): The ID of the list to create the task in.
            name (str): The name of the task to create. Defaults to 'Test API Task'.
            description (str): The description of the task to create. Defaults to ''.
            custom_task_ids (bool, optional): Whether to use custom task IDs. Defaults to True.
            team_id (str, optional): The ID of the team to create the task in. Defaults to ''.
            tags (list, optional): The tags to add to the task. It requires only the name of the tags and automatically formats those tags, with random colors, to be used in the created task. Defaults to [].
            status (str, optional): The status of the task to create. It requires only the name of the tags and automatically formats those tags, to be used in the created task. Defaults to 'new'.

        Returns:
            _type_: A dictionary containing the response from the API.
        """
        url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
        query = {
            "custom_task_ids": str(custom_task_ids).lower(),
            "team_id": team_id,
        }
        payload = {
            "name": name,
            "description": description,
            "tags": tags,
            "status": status,
            "parent": parent,
        }
        response = None
        while response is None:
            try:
                response = post(url, json=payload, headers=self.headers, params=query)
            except:
                # Handle connection error, and try again in 1 second
                pass
            sleep(1)
        return response.json()

    def update_task_status(self, task_id: str, status: str) -> dict:
        """Updates the status of a given task.

        Args:
            task_id (str): The ID of the task to update.
            status (str): The new status of the task.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        url = f"https://api.clickup.com/api/v2/task/{task_id}"
        payload = {
            "status": status,
        }
        response = None
        while response is None:
            try:
                response = put(url, json=payload, headers=self.headers)
            except:
                # Handle connection error, and try again in 1 second
                pass
            sleep(1)
        try:
            return response.json()
        except JSONDecodeError as e:
            # Log the error and return an empty dictionary
            print(f"Task URL: {url}. Error decoding JSON response: {e}")
            return {}

    def get_all_folderless_lists(self, space_id: str) -> dict:
        """Retrieves all folderless lists from a given space.

        Args:
            space_id (str): The ID of the space to retrieve folderless lists from.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        all_lists = []
        page = 0
        url = f"https://api.clickup.com/api/v2/space/{space_id}/list"
        while True:
            tqdm.write(f"Downloading page {page}")
            query = {
                "page": str(page),
            }
            response = None
            while response is None:
                try:
                    response = get(url, headers=self.headers, params=query)
                except:
                    # Handle connection error, and try again in 1 second
                    pass
                sleep(1)
            data = response.json()

            if data["lists"] == []:
                break
            all_lists.extend(data["lists"])
            page += 1
        return dict(lists=all_lists)

    def get_all_folder_list(self, folder_id: str) -> dict:
        """Retrieves all lists from a given folder.

        Args:
            folder_id (str): The ID of the folder to retrieve lists from.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        url = f"https://api.clickup.com/api/v2/folder/{folder_id}/list"
        response = None
        while response is None:
            try:
                response = get(url, headers=self.headers)
            except:
                # Handle connection error, and try again in 1 second
                pass
            sleep(1)
        return response.json()
