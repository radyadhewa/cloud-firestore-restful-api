# REST API with Flash(Python) to Firebase Firestore(Google) 🌎🚀

To run the project there are 2 ways:
1. [Clone this repository](#via-github-repository)
2. [Pull the docker image](#via-docker-pull)

[Proceed to endpoint documentation](#end-points)

---
## Via Github Repository
#### 1. Clone the project & navigate to the directory 🔗
```
git clone https://github.com/radyadhewa/cloud-firestore-restful-api
```
```
cd cloud-firestore-restful-api
```
#### 2. You will need to install the necessary dependencies 🖥
```
pip install -r requirement.txt
```

#### 3. For the use of this REST API, you will need to download the Firebase credentials from your Firebase console 🤓
> Or if you want to access our database please pull docker image or request access on this [google drive](https://drive.google.com/drive/folders/1YjlUzDCbbPScoBm2e6H2Zx9vtOyvj0db?usp=drive_link) link for the key file

To create your database and it's key:
- Go to [Firebase](https://console.firebase.google.com/) 
- Create a new project 
- Create Firestore database in production or test mode
- In the project select > Project settings > Service accounts > python
- Select "Generate new private key"
- Add the created & downloaded file to "api" folder of this project 
- Rename the file to "key.json" 

#### 4. Now you can now run the API and check the end-points documentation 🖥
```
python main.py
```
<br>

## Via Docker Pull
#### 1. Install [Docker](https://docs.docker.com/desktop/) (if you don't have it yet) 🐋
#### 2. Pull the image & run via preferable terminal 💿
```
docker pull radyadhewa/restful_firestore
```
```
docker run -d -p 5000:5000 radyadhewa/restful_firestore
```
#### 3. Open localhost:5000 and try the endpoints via postman or etc 💻
<br>

---

## End-points

route http://127.0.0.1:5000/ will render the documentation

<h5><font color="green">football ticket API</font></h5>
 
route http://127.0.0.1:5000/ticket will render the key value on ticket database

route http://127.0.0.1:5000/ticket/add we can add users by POST method

route http://127.0.0.1:5000/ticket/retrieve will retrieve all ticket data and join country data from stadium database by GET method

route http://127.0.0.1:5000/ticket/update/{id} to update a ticket data by PUT method and DELETE it if stock = 0
  requires data id to be fill

route http://127.0.0.1:5000/ticket/deletetiket/{id} to delete a ticket data by DELETE method
  requires id to delete

route http://127.0.0.1:5000/ticket/uniqueteams to get all teams list in the ticket database by GET method (unique no duplicate)

route http://127.0.0.1:5000/ticket/join to get all data from both database by GET method (ticket + stadium database)

the route http://127.0.0.1:8000/modName we can modify the name of the user Requires user id

<h5><font color="purple">stadium list API</font></h5>

route http://127.0.0.1:5000/stadium will render the key value on stadium database

route http://127.0.0.1:5000/stadium/retrieve will retrieve all stadium database by GET method

route http://127.0.0.1:5000/stadium/deletestadium/{id} to delete a stadium data by DELETE method
  requires data id to be fill
