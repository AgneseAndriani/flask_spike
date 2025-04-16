# Per iniziare

- Installa i requisiti:
```bash
  pip install -r requirements.txt
  ```
---

## DB Creation
- Root user = root
- PW = root
- db = mydatabase


#### Init (and start MySQL with same fake data)
```
  sh docker-init.sh
  ```


#### Stop MySQL database (Keeps data)
```
  sh docker-stop.sh
  ```

#### Start MySQL database
```
  sh docker-start.sh
  ```


---
## How to use
Simil POSTMAN:
https://hoppscotch.io/

```
  GET (all users)
  http://127.0.0.1:5000/test-get-all-users
  ```

```
  GET (user by ID)
  http://127.0.0.1:5000/test-get-user
  
  Params: user_id
  
  Example:
  user_id = 1
  ```

```
  POST (new user)
  http://127.0.0.1:5000/add-user
  
  Body : user (json format)
  
  Example:
  {"user" : {"name":"test_user", "email": "test@test.it"}}
  ```
