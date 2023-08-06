# zendesk-clickup
Project that syncs all tickets from Zendesk to ClickUp. This is useful for teams that use them for managing customer support tickets and want to keep the ticket numbers consistent across both platforms.

## Installation
This module is available on PyPI and can be installed using pip.
```bash
$ python -m pip install syncticketstoclickup
```
This module requires Python 3.10 or higher.

## Configuration
1. Duplicate the `.env.example` file and rename it to `.env`.
2. Replace the placeholder values in the `.env` file with your actual configuration.

## Usage
This is the basic usage of the module to sync all tickets from Zendesk to ClickUp.
```python
from syncticketstoclickup.zendesk_to_clickup import ZendeskToClickUp

ZendeskToClickUp().sync_zendesk_to_clickup()
```