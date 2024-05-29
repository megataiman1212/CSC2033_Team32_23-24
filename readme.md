

Repository URL:
https://github.com/newcastleuniversity-computing/CSC2033_Team32_23-24.git

---
Instruction for setting up Database
---
1. Install Dependencies
 - Docker Desktop: https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe
 - Install mySql Workbench (Optional for access to database without website): https://dev.mysql.com/downloads/file/?id=525959
 - Use pycharm IDE as integration with docker: https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=windows
 - Install all python requirements in requirements.txt (Pycharm should automatically ask to install) , To manually install use "py pip install" then the name of the requirement
2. Through pycharm Run the Create_Database/docker-compose.yml file by pressing the green arrow
 - This should install the mysql image for docker and start running the database
 - Check in the services tab of pycharm that there is a docker compose connection with a subitem called "db". If db is not running; Run it and wait till the console says "X plugin ready for connections"
 - If you have a mysql server running in the background using the localhost address before this then you will need to stop it
3. Once the database is started you can run the Create_Database/create_db.py file then the Create_Database/create_tables.py file
4. The database should now be setup to connect to it through mysql workbench use Hostname:127.0.0.1 port:3306 and password "Team32"
5. To start the website run the app.py file in pycharm and click the blue link in the console

Create_Database/create_db.py will reset the database and add an admin user everytime it is run

On restart simply run the database through the services tab in pycharm

---
Coding Standards
---
For our coding standards we have been using Pylint integrated into the github workflow and also pycharms inbuilt linting.
We have also agreed to other standards which are outlined in the further documentation

---
For more Documentation we have included a file !!FILENAMEHERE!!
---

