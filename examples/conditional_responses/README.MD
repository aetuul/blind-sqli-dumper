# Identifying successful requests via conditional responses
## Payload
In this example, the server provided a slightly different response for successful injections, returning a `Welcome back` message on successful requests. This allows us to identify successful requests by examining the response body.
`FUZZ1` represents the current guessing index in the password field, while `FUZZ2` is the actual guess.
## Request
The vulnerability was found in the request cookie `TrackingId`, thus the keyword `FUZZ` is placed in the `TrackingId` field.