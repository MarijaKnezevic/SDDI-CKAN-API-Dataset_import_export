# Export CKAN Users to Excel Script
The Python script exports a list of all users from a CKAN instance into an Excel file. The script fetches user details such as ID, username, email, state and created, and saves them in a structured Excel file.

## Functionality of the *Export CKAN Users to Excel Script*
1. Clone or download the repository containing the script.
2. Update the following fields in the script:
- Replace `ckan_url` with your CKAN instance URL.
  For example: `ckan_url = "http://your-ckan-instance-url"`
- Replace `api_key` with your CKAN admin API key.
  For example: `api_key = "your-admin-api-key"`
3. Run the script from your terminal or command prompt:
  
   `python export_ckan_users_to_excel.py`



# Soft-Delete CKAN Users Script and Export CKAN Users to Excel Script

The Python script is designed to soft-delete (deactivate) users in a CKAN instance by setting their state to deleted. The script fetches all users from the CKAN instance, identifies the target users by their usernames, and updates their state to deleted.
The soft-deletion does not permanently remove users but marks them as inactive, preserving the data while disabling the user’s access.

## Functionality of the *soft delete ckan users* scrypt
1. Clone or download the repository containing the script.
2. Update the following fields in the script:
- Replace `ckan_url` with your CKAN instance URL.
  For example: `ckan_url = "http://your-ckan-instance-url"`
- Replace `api_key` with your CKAN admin API key.
  For example: `api_key = "your-admin-api-key`
3. List the usernames you want to soft-delete in the `usernames_to_delete` list. For example:
  
   `usernames_to_delete = ["username1", "username2"]`
4. Run the script from your terminal or command prompt:
  
   `python soft_delete_ckan_users.py`
5. If successful, you will see a message confirming the users have been soft-deleted:
  
   `User [user_id] soft-deleted successfully.`
