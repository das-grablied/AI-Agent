import os
from config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory, file_path):

    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(abs_working_dir, file_path))
        valid_target_file = os.path.commonpath(
            [abs_working_dir, target_file]) == abs_working_dir

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f"Error: File not found or is not a regular file: {file_path}"

        with open(target_file, 'r') as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Prints the content of the target file, truncating it at 10,000 characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the target file",
            ),
        },
        required=["file_path"],
    ),
)
