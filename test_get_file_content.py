from functions.get_file_content import get_file_content

result = get_file_content("calculator", "lorem.txt")
assert "[...File" in result and "truncated" in result
print(f"Content length: {len(result)}")
print(result[-100:])

result = get_file_content("calculator", "main.py")
print(result)

result = get_file_content("calculator", "pkg/calculator.py")
print(result)

result = get_file_content("calculator", "/bin/cat")
print(result)

result = get_file_content("calculator", "pkg/does_not_exist.py")
print(result)
