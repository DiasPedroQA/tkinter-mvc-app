# import re
# from datetime import datetime


# def validate_email(email: str) -> bool:
#     """Validates the format of an email address."""

#     pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
#     return re.match(pattern, email) is not None


# def format_date(date: str, current_format: str, desired_format: str) -> str:
#     """Formats a date string from current_format to desired_format."""

#     try:
#         parsed_date = datetime.strptime(date, current_format)
#         return parsed_date.strftime(desired_format)
#     except ValueError:
#         return ""


# def sanitize_input(input_string: str) -> str:
#     """Sanitizes input by stripping whitespace and removing special characters."""

#     return re.sub(r"[^\w\s]", "", input_string.strip())
