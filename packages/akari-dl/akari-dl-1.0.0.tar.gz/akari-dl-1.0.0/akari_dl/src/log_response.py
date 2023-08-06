def log_response(response):
  """
    Log response headers and html into .log files (for development purpose).
  """
  with open("HEADERS.log", "w", encoding="utf-8") as header_dump:
    header_dump.write(str(response.headers))
  with open("BODY.log", "w", encoding="utf-8") as body_dump:
    body_dump.write(str(response.text))
