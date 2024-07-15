# Time based using `pg_sleep()` to identify successful requests
## Payload
In this example, the purpose of the payload is to make the backend server sleep for a specified number of seconds. By leveraging PostgreSQL's pg_sleep() function, we can identify successful requests.<br>
`FUZZ1` represents the current guessing index in the password field, while `FUZZ2` is the actual guess.
## Request
The vulnerability was found in the request cookie `TrackingId`, thus the keyword `FUZZ` is placed in the `TrackingId` field.