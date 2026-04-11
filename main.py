import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError(
            "GEMINI_API_KEY not found in environment variables. Please set it in the .env file.")

    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="AI Agent")

    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output")

    args = parser.parse_args()
    messages = [types.Content(
        role="user", parts=[types.Part(text=args.user_prompt)])]

    generate_content(client, messages, args.verbose, args.user_prompt)


def generate_content(client, messages, verbose, user_prompt):
    for _ in range(20):  # Limit to 20 iterations to prevent infinite loops

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt),
        )

        if response.candidates is not None and len(response.candidates) > 0:
            messages.append(response.candidates[0].content)

        if response.function_calls is None:
            print(response.text)
            return

        if response.usage_metadata is None:
            raise RuntimeError("Response does not contain usage metadata.")

        metadata = response.usage_metadata

        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {metadata.prompt_token_count}")
            print(f"Response tokens: {metadata.candidates_token_count}")

        if response.function_calls:
            function_results = []

            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose)

                if function_call_result.parts is None:
                    raise Exception(
                        "Function call result does not contain parts.")
                if function_call_result.parts[0].function_response is None:
                    raise Exception(
                        "Function call result part does not contain function response.")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception(
                        "Function call result part does not contain function response data.")

                function_results.append(function_call_result.parts[0])

            if verbose:
                print(
                    f"-> {function_results[0].function_response.response}")

            messages.append(types.Content(
                role="user", parts=function_results))

        if _ == 19:  # Last iteration
            print("Reached maximum number of iterations. Stopping...")
            sys.exit(1)

    else:
        print(response.text)


if __name__ == "__main__":
    main()
