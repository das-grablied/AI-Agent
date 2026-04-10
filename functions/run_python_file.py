import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):

    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(abs_working_dir, file_path))
        valid_target_file = os.path.commonpath(
            [abs_working_dir, target_file]) == abs_working_dir
        absolute_file_path = os.path.abspath(target_file)

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", absolute_file_path]

        if args:
            command.extend(args)

        output = subprocess.run(
            command, cwd=abs_working_dir, capture_output=True, text=True, timeout=30)
        output_string = []

        if output.returncode != 0:
            output_string.append(
                f"Process exited with code {output.returncode}")

        if not output.stdout and not output.stderr:
            output_string.append("No output produced")

        if output.stdout:
            output_string.append(f"STDOUT:\n{output.stdout}")

        if output.stderr:
            output_string.append(f"STDERR:\n{output.stderr}")

        return "\n".join(output_string)

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the target Python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the target Python file",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="A list of arguments for the target Python file",
            )
        },
        required=["file_path"],
    ),
)
