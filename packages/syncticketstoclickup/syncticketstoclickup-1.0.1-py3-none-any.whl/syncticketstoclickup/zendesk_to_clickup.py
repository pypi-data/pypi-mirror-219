from syncticketstoclickup.zendesk import ZendeskAPI
from syncticketstoclickup.clickup import ClickUpAPI
from os import getenv
from re import search
from tqdm import tqdm
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file


class ZendeskToClickUp:
    """This class represents the main class for the Zendesk to ClickUp sync."""

    def __init__(self) -> None:
        self.zendesk_api_key = self.get_env_var("ZENDESK_API_KEY")
        self.subdomain = self.get_env_var("ZENDESK_SUBDOMAIN")
        self.email = self.get_env_var("ZENDESK_EMAIL")
        self.clickup_api_key = self.get_env_var("CLICKUP_API_KEY")
        self.list_id = self.get_env_var("CLICKUP_LIST_ID")
        self.space_id = self.get_env_var("CLICKUP_SPACE_ID")
        # Initialize the API clients
        self.zendesk_api = ZendeskAPI(self.zendesk_api_key, self.subdomain, self.email)
        self.clickup_api = ClickUpAPI(self.clickup_api_key)

    def get_env_var(self, name: str) -> str:
        """Get the value of an environment variable.

        Args:
            name (str): The name of the environment variable.

        Returns:
            str: The value of the environment variable.
        """
        value = getenv(name)
        if value is None:
            raise ValueError(f"Environment variable {name} is not set.")
        return value

    def status_formatter(self, custom_status_id: str) -> str:
        """This function converts the custom status ID from Zendesk to the status name in ClickUp.
            It's used instead of just the status field because the status field is not always accurate.
            The IDs are from the custom statuses in Zendesk and they are not the same for every Zendesk account.

        Args:
            custom_status_id (str): The custom status ID from Zendesk.

        Returns:
            str: The status name in ClickUp.
        """
        status_relationship = {
            "1900007244545": "new",
            "1900007244565": "open",
            "1900007244585": "pending",
            "9356055796375": "in repair",
            "1900007244625": "closed",  # Same ID for solved and closed status in Zendesk
        }
        return status_relationship.get(custom_status_id, "new")

    def create_clickup_task(self, list_id: str, ticket: dict) -> None:
        """Create a task in ClickUp for a ticket.

        Args:
            list_id (str): The ID of the list to create the task in.
            ticket (dict): The ticket to create a task for.
        """
        url = ticket["url"].replace("api/v2", "agent").rstrip(".json")
        task_name = f"TN: {ticket['id']:06} - {ticket['subject']}"  # :06 pads the ticket ID with 0s to 6 digits
        task_description = f"{url}\n\nDESCRIPTION:\n{ticket['description'].strip()}"
        self.clickup_api.set_new_task(
            list_id=list_id,
            name=task_name,
            description=task_description,
            tags=ticket["tags"],
            status=self.status_formatter(str(ticket["custom_status_id"])),
        )

    def format_ticket_number(self, tn: str) -> str:
        """Formats a ticket number to a 6-digit string.

        Args:
            tn (str): The ticket number to format.

        Returns:
            str: The formatted ticket number as a 6-digit string.
        """
        return f"{tn:06}"

    def sync_zendesk_to_clickup(self):
        """Syncs tickets from Zendesk to ClickUp by creating new tasks for new tickets and updating the status of existing tasks
        based on the status of the corresponding tickets in Zendesk.
        """
        # Call the method to get tickets
        tickets = self.zendesk_api.get_all_tickets()
        all_tasks = self.clickup_api.get_all_tasks(
            list_id=self.list_id, include_closed=True
        )
        all_tasks_tn_id = {
            search(r"\d+", task["name"]).group(): task["id"]
            for task in all_tasks["tasks"]
        }
        tickets_not_in_clickup = [
            self.format_ticket_number(ticket["id"])
            for ticket in tickets["tickets"]
            if self.format_ticket_number(ticket["id"]) not in all_tasks_tn_id.keys()
        ]
        # Loop for all tickets. Existing tickets will be updated and new tickets will be created
        for ticket in tqdm(
            tickets["tickets"], desc="Comparing tickets and tasks", colour="green"
        ):
            if self.format_ticket_number(ticket["id"]) in tickets_not_in_clickup:
                # Ticket is in new_tickets, create a task in ClickUp
                tqdm.write(f"CREATING: {self.format_ticket_number(ticket['id'])}")
                self.create_clickup_task(list_id=self.list_id, ticket=ticket)
            else:
                # Ticket is not new, check if status is different from the one in ClickUp and update it
                # Update the status of the task and exclude the ones that are already closed
                if (
                    self.format_ticket_number(ticket["id"]) in all_tasks_tn_id.keys()
                ) and (
                    all_tasks_tn_id[self.format_ticket_number(ticket["id"])] != None
                ):
                    task_info = self.clickup_api.get_task(
                        task_id=all_tasks_tn_id[self.format_ticket_number(ticket["id"])]
                    )
                    if "status" in task_info:
                        old_status = str(task_info["status"]["status"]).lower().strip()
                    else:
                        old_status = ""
                        print(task_info)
                    new_status = self.status_formatter(
                        str(ticket["custom_status_id"]).lower().strip()
                    )
                    # Updates the status of the task if it is different from the one in ClickUp
                    if new_status != old_status:
                        tqdm.write(
                            f"UPDATING STATUS: {self.format_ticket_number(ticket['id'])} from {old_status} to {new_status}"
                        )
                        self.clickup_api.update_task_status(
                            task_id=all_tasks_tn_id[
                                self.format_ticket_number(ticket["id"])
                            ],
                            status=new_status,
                        )
        now = datetime.now()
        formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        tqdm.write(
            f"Finished syncing Zendesk Tickets to ClickUp at {formatted_date_time}"
        )
