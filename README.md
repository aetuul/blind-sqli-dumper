# Automated Blind SQLi Data Dumper
## Overview
This project is a Python-based tool designed to automate the process of data dumping via blind SQL injections using binary search to narrow down the count of requests. Originally created for CTF purposes.
Some example payloads and requests can be found in /examples
## Features
- Easy configuration through `payload.txt` and `request.req`
- Match by status code, response body or time
## Requirements
- Python 3.x
- Working payload
- Working copy of a request to vulnerable page
## Installation
1. Clone the repository:<br>
`git clone https://github.com/aetuul/blind_dumper.git`<br>
`cd blind_dumper`
2. Install the required Python libraries<br>
`pip install -r requirements.txt`
## Configuration
1. Configure `payload.txt` - Replace the value you want to fuzz with the keyword `FUZZ2` and the index with `FUZZ1`
2. Configure `request.req` - Easiest way is to copy the exploit request from Burp Suite. Insert the keyword FUZZ into your request where the payload should go
## Usage
`python3 dump.py <args>`
## Arguments
-req (required): Path to the .req file used for making the requests<br>
-target (required): The target URL<br>
-payload (required): The payload to use with fuzzing values<br>
-length (required): The length of the data you're trying to dump<br>
-mc (optional): HTTP status code to indicate a successful request<br>
-fc (optional): HTTP status code to indiace a failed request<br>
-mb (optioal): Text in the HTTP response body to indicate a successful request<br>
-mt (optional): HTTP response duration in seconds to indicate a successful request<br>
-pi (optional): Proxy server ip<br>
-pp (optional): Proxy server port<br>
## Example usage
1. Dump data from the target using the specified request and payload, expecting the data length to be 20 characters, using HTTP status code 500 to identify successful requests and HTTP status code 200 to identify "failed" requests
`python3 dump.py -req request.req -target "https://<target>" -payload payload.txt -length 20 -mc 500 -fc 200`

2. Extract data from the target using the specified request and payload, expecting a data length of 20 characters and identifying successful responses by the keyword "Welcome back" in the HTTP response body
`python3 dump.py -req request.req -target "https://<target>" -payload payload.txt -length 20 -mb "Welcome back"`

3. Extract data from the target using the specified request and payload, expecting a data length of 20  characters and identifying successful responses by the response time<br>
`python3 dump.py -req request.req -target "https://<target>" -payload payload.txt -length 20 -mt 5`
Note that when identifying requests by the response time, the payload needs to use `>=` instead of `=`.
## Disclaimer
Education purposes only.
