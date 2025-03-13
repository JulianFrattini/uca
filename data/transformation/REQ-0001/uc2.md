```mermaid
sequenceDiagram

actor user AS User

participant gui AS GUI

user ->> gui : open landing page
gui -->> user : landing page
user ->> gui : access login form 
gui -->> user : login form
user ->> gui : submit credentials

alt credentials correct
    gui -->> user : authenticate and forward to internal page
else credentials incorrect
    gui -->> user : display error
end
```