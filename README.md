# Automated Blind SQLi Data Dumper
## Overview
This project is a Python-based tool designed to automate the process of data dumping via blind SQL injections using binary search to narrow down the count of requests.
Some example payloads and requests can be found in /examples
## Features
- Easy configuration through `payload.txt` and `request.req`
- Match by status code or response body
## Requirements
- Python 3.x
- Working payload
- Working copy of a request to vulnerable page
## Installation
1. Clone the repository:
`git clone https://github.com/aetuul/blind_dumper.git`
`cd blind_dumper`
2. Install the requited Python libraries
`pip install -r requirements.txt`
## Configuration
1. Configure `payload.txt` - Replace the value you want to fuzz with the keyword `FUZZ2` and the index with `FUZZ1`
2. Configure `request.req` - Easiest way is to copy the exploit request from Burp Suite. Insert the keyword FUZZ into your request where the payload should go
## Usage
`python3 dump.py -req <path_to_req_file> -target <target_url without endpoint> -payload <path_to_payload_file> -length <data_length> [-mc <http_status_code>] [-mt <response_text>]`
## Arguments
-req (required): Path to the .req file used for making the requests.
-target (required): The target URL.
-payload (required): The payload to use with fuzzing values.
-length (required): The length of the data you're trying to dump.
-mc (optional): HTTP status code to indicate a successful request.
-mt (optional): Text in the HTTP response to indicate a successful request.
## Example usage
1. Dump data from the target using the specified request and payload, expecting the data length to be 20 characters and using HTTP status code 500 to identify successful requests
`python3 dump.py -req request.req -target "https://<target>" -payload payload.txt -length 20 -mc 500`
2. Extract data from the target using the specified request and payload, expecting a data length of 20 characters and identifying successful responses by the keyword "Welcome back" in the HTTP response body
`python3 dump.py -req request.req -target "https://<target>" -payload payload.txt -length 20 -mt "Welcome back"`
## Disclaimer
Education purposes only.
