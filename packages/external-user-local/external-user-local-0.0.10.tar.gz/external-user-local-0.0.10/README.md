# External User Local Python Package

The External User Local Python Package is a library designed to manage access tokens for external users. It provides functions to insert, update, retrieve, and delete access tokens from a database. This library is intended to be used in conjunction with your own project.

## Installation

-pip install External-User-Local 0.0.1
-add to requirments External-User-Local==0.0.1

# Importing the Library
from library import library_DB import Accsess_Token_Library
# Usage Example:
# Initialize the access token library
access_token_lib = Accsess_Token_Library()

# Insert a new access token
access_token_lib.insert_user_external("example_user", 123, "example_token")

# Update an existing access token
access_token_lib.update_user_external(123, "updated_token")

# Retrieve an access token by profile ID
access_token = access_token_lib.get_access_token(123)

# Retrieve an access token by user name
access_token = access_token_lib.get_access_token_by_user_name("example_user")

# Delete an access token by profile ID
access_token_lib.delete_access_token_by_profile_id(123)

# Update an existing access token by username
access_token_lib.update_user_external_by_username("example_user", "new_token")

