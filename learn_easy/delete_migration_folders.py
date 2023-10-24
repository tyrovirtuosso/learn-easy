import os
import shutil

def delete_migration_folders(project_dir: str) -> None:
    """
    Recursively deletes the 'migrations' folders in all app directories within the specified project directory.

    :param project_dir: The path to the Django project directory.
    :type project_dir: str
    """
    # Get a list of all directories in the project directory
    all_dirs = os.listdir(project_dir)

    for app_name in all_dirs:
        # Construct the path to the migrations directory of the app
        migrations_dir = os.path.join(project_dir, app_name, 'migrations')

        # Check if the migrations directory exists
        if os.path.exists(migrations_dir):
            print(f"Deleting entire migrations folder for app '{app_name}'")
            try:
                # Use shutil.rmtree to remove the entire directory, including its contents
                shutil.rmtree(migrations_dir)
            except OSError as e:
                print(f"Error deleting migrations folder for app '{app_name}': {e}")

if __name__ == "__main__":
    # Specify the project directory where all your apps are located
    project_directory = os.path.dirname(os.path.abspath(__file__))  # Assumes this script is in the project directory

    # Call the function to delete migration folders for all apps
    delete_migration_folders(project_directory)
