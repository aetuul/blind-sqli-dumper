# Conditional errors leveraging `division by zero error`
## Payload
In this example, the payload is designed to cause the backend server to encounter a division by zero error by attempting to evaluate the mathematical expression 1/0. This caused the server to return a `500 Internal server error` providing us a simple way to identify successful requests via response status codes. <br>
`FUZZ1` represents the current guessing index in the password field, while `FUZZ2` is the actual guess.
## Request
The vulnerability was found in the request cookie `TrackingId`, thus the keyword `FUZZ` is placed in the `TrackingId` field.