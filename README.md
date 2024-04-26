# Mood Journal

## Setup 
### Client
To install client dependencies and start client, open up a new terminal and run
```bash
cd client
yarn install
yarn run dev
```
Your frontend should now be visible -- visiting the link provided by Vite in your terminal will show a simple Twitter mockup!

### Server
Create a PostgreSQL database called `journal`. To configure the database connection, create a `.env` file in the `root` directory with the following content: 
```
SQLALCHEMY_DATABASE_URI = "postgresql://localhost/journal"
```

Now create a virtual environment, install dependencies, and start the server in a separate terminal window with 
```bash
cd server
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
flask run
```