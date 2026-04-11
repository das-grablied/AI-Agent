import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))
        valid_target_dir = os.path.commonpath(
            [abs_working_dir, target_dir]) == abs_working_dir

        if not valid_target_dir:
            return f"Error: Cannot list {directory} as it is outside the permitted working directory"

        if not os.path.isdir(target_dir):
            return f"Error: {directory} is not a directory"

        files_info = []

        for item in os.listdir(target_dir):
            item_name = os.path.basename(item)
            item_size = os.path.getsize(os.path.join(target_dir, item))
            is_dir = os.path.isdir(os.path.join(target_dir, item))

            files_info.append(
                f"- {item_name}: file_size={item_size} bytes, is_dir={is_dir}")

        return "\n".join(files_info)

    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the target directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
