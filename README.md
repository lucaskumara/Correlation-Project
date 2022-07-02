# Correlation-Project
A simple application to calcuate correlations between USD/CAD exhange rates and CORRA rates for a coderbyte submission.

## How to run
The repository contains code for both the frontend GUI and backend API. The application uses React for the front end GUI and Flask for the backend API. Clone the repository and use two terminals to run the frontend and backend applications. Instructions to run them are listed below.

### Backend
1. Navigate to the backend directory using `cd backend`
2. Create a python virtual environment using `python3 -m venv env` (you may be able to use `python` instead of `python3` on windows)
3. Activate the virtual environment using `source env/bin/activate` (or `.\env\Scripts\activate` on windows)
4. Install the python dependencies using `pip install -r requirements.txt`
5. Run the flask application using `flask run`

Flask should now be up and running on localhost:5000

### Frontend
1. Navigate to the frontend directory using `cd frontend`
2. Install packages using `npm install`
3. Run the react application using `npm start`

The react app should be running on localhost:3000

### Usage
Once you have the React and Flask apps running, go to localhost:3000 in your browser and you should be able to input two dates and have the calculations displayed to you upon submission.
