from requests import get, post
from base64 import b64encode
from tqdm import tqdm
from time import sleep
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file


class ZendeskAPI:
    """This class represents an API client for the Zendesk API."""

    def __init__(self, api_key: str, subdomain: str, email: str) -> None:
        """Initializes the API client.

        Args:
            api_key (str): The API key for the Zendesk account.
            subdomain (str): The subdomain of the Zendesk account.
            email (str): The email address associated with the Zendesk account.
        """
        self.api_key = api_key
        self.email = email
        self.base_url = f"https://{subdomain}.zendesk.com/api/v2"
        self.headers = {
            "Authorization": f"Basic {self._get_encoded_auth_string()}",
            "Content-Type": "application/json",
        }

    def _get_encoded_auth_string(self) -> str:
        """Returns the encoded authentication string for the API client.

        Returns:
            str: The encoded authentication string.
        """
        auth_string = f"{self.email}/token:{self.api_key}"
        return b64encode(auth_string.encode()).decode()

    def get_all_tickets(self) -> dict:
        """Retrieves all the tickets from the Zendesk account.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        all_tickets = []
        page = 1
        while True:
            endpoint = f"{self.base_url}/tickets.json?page={page}"
            response = get(endpoint, headers=self.headers)
            tickets = response.json().get("tickets", [])
            all_tickets.extend(tickets)
            tqdm.write(f"Downloaded {len(tickets)} tickets from page {page}")
            if not response.json().get("next_page"):
                break
            page += 1
            sleep(1)  # Wait for 1 second before making the next API request
        tqdm.write(f"Downloaded {len(all_tickets)} tickets in total")
        return dict(tickets=all_tickets)

    def get_specific_ticket(self, ticket_id: int) -> dict:
        """Retrieves a specific ticket from the Zendesk account.

        Args:
            ticket_id (int): The ID of the ticket to retrieve.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        url = f"{self.base_url}/tickets/{str(ticket_id)}.json"
        response = get(url, headers=self.headers)
        return response.json()

    def get_all_tags(self) -> dict:
        """Retrieves all the tags from the Zendesk account.

        Returns:
            dict: A dictionary containing the response from the API.
        """
        url = f"{self.base_url}/tags.json"
        response = get(url, headers=self.headers)
        return response.json()

    def set_new_ticket(
        self,
        subject: str,
        description: str,
        requester_id: str,
        submitter_id: str,
        tags: list = [""],
    ) -> dict:
        """Creates a new ticket in the Zendesk account.

        Args:
            subject (str): The subject of the new ticket.
            description (str): The description of the new ticket.
            requester_id (str): The ID of the requester for the new ticket.
            submitter_id (str): The ID of the submitter for the new ticket.
            tags (list, optional): The tags for the new ticket. Defaults to [''].

        Returns:
            dict: A dictionary containing the response from the API.
        """
        ticket_data = {
            "ticket": {
                "subject": subject,
                "description": description,
                "requester_id": requester_id,
                "submitter_id": submitter_id,
                "tags": tags,
                "organization_id": 1500418008861,
                "group_id": 1500001046461,
            }
        }
        endpoint = f"{self.base_url}/tickets.json"
        response = post(endpoint, headers=self.headers, json=ticket_data)
        return response.json()
