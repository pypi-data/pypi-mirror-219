import os
import ast
import sys
import inspect
import pymsgbox as msgbox


class SecretChecker:

    def __init__(self, file_path=None, folder_name="app" , env_list=["prod", "production"], env_key_list = ["env", "environment"], button_values = ["OK", "Cancel"]):

        # if the environment is prod / production then we don't need to show the pop-up 
        # self.env_key_list = env_key_list 
        
        self.file_path = file_path
        self.env_list = env_list
        self.button_display_options = button_values

        # print("file path : ", self.file_path)

        if self.file_path:
            self._check_secrets_with_specific_values()
        elif folder_name and folder_name == "app": 
            # print("need to fetch all the files in the current directory")
            self._fetch_all_files_in_same_directory()
        else:
            self._fetch_all_files_in_folder(folder_name)
    

    def _fetch_all_files_in_same_directory(self):
        
        current_directory = os.getcwd()
        files_list = [os.path.join(current_directory, file) for file in os.listdir(current_directory) if os.path.isfile(os.path.join(current_directory, file))]

        # print("files list : ", files_list)

        self._iterate_through_files(files_list)
    

    def _fetch_all_files_in_folder(self, folder_name="app"):
        
        folder = folder_name # Specify the folder path within the project directory

        # print("folder : ", folder)
        
        current_file = inspect.getframeinfo(inspect.currentframe()).filename
        project_directory = os.path.dirname(os.path.abspath(current_file))
        folder_path = os.path.join(project_directory, folder)

        files_list = []
        for root, dirs, files in os.walk(folder_path):
            if "__pycache__" in dirs:
                dirs.remove("__pycache__")  # Skip files in the __pycache__ directory
            for file in files:
                file_path = os.path.join(root, file)
                files_list.append(file_path)

        self._iterate_through_files(files_list)

    
    def _iterate_through_files(self, files):

        # Print all file paths
        for file in files:
            self.file_path = file
            # print("==== ", file)
            self._check_secrets_with_specific_values()


    def _check_secrets_with_specific_values(self):
        
        with open(self.file_path, 'r') as file:
            tree = ast.parse(file.read())

            constants = []

            for node in ast.walk(tree):

                if isinstance(node, ast.Assign) and len(node.targets) == 1:
                    target = node.targets[0]
                    
                    if isinstance(target, ast.Name) and target.id.isupper():

                        secret_val = ast.literal_eval(node.value)

                        if any(word in str(secret_val).lower() for word in self.env_list):
                            button_val = msgbox.confirm(f"SECRET {target.id} = {secret_val} found in {self.file_path}. Do you wish to continue?", "Trying to access prod resource", buttons=self.button_display_options)
                            
                            if button_val in ["No", "Cancel"]:
                                sys.exit(1)
                            
                            # print("Do you wish to continue ? ", button_val)

                        constants.append(target.id)
            
        



