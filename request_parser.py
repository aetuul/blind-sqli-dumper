def read_req_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Split headers and body
    header_lines, body = [], []
    is_body = False
    for line in lines:
        if is_body:
            body.append(line)
        elif line == '\n':
            is_body = True
        else:
            header_lines.append(line)
    
    return header_lines, body

def parse_headers(header_lines, payload):
    method, url = None, None
    headers = {}
    
    for line in header_lines:
        if line.startswith(('GET', 'POST', 'PUT', 'DELETE', 'PATCH')):
            parts = line.split()
            method, url = parts[0], parts[1]
        else:
            line = line.replace("FUZZ", payload)
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()
    
    return method, url, headers



