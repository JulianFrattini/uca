```mermaid
sequenceDiagram

actor user AS User

participant gui AS GUI

user ->> gui : access registration form 
gui -->> user : registration form
user ->> gui : submit information

loop while password does not comply to requirements
    gui -->> user : inform about password requirements
end

alt email address not in use yet
    gui -->> user : authenticate and forward to internal page
else credentials incorrect
    gui -->> user : display error
end
```