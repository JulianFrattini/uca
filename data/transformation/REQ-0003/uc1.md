```mermaid
sequenceDiagram

actor user AS (Operator)

participant gui AS GUI
participant udb AS User Data Base

user ->> gui : access user overview
gui ->> udb : retrieve user list
udb -->> gui : user list
gui -->> user : list users
```