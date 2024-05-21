# gotc-online
A Web App to play the Guardians Of The City 2 (GOTC) card game

## What is GOTC
Guardians Of The City is a card game designed by MINDEF Singapore. 

It is a Total Defence strategy card game designed to help youths develop a deeper understanding of Singapore security threats and the part we play in keeping Singapore safe and secure. The card game presents different security threats as crises and illustrates how the six pillars of Total Defence can be applied to respond to and recover from the crises.

For more information, refer to the official website for GOTC: https://www.mindef.gov.sg/oms/imindef/mindef_websites/topics/totaldefence/resources-guardians-of-the-city.html

## What is GOTC Online
GOTC Online is a project to create a way for people to play GOTC with each other through the internet, providing a way for people to play even if they can't be in the same place at the same time. 

The authors of this project are not affiliated with MINDEF and are not developing this project out of financial incentive.

## How it works
GOTC Online is a website. The repository is split into two folders, one for the frontend and one for the backend.

The frontend uses the Vue framework and is written in TypeScript.<br>
To run a development server, use `npm run dev` in the frontend directory.<br>
Deploy using `npm run build` in the backend directory and the built project will be in the dist folder. 
Use web server to serve `index.html` from the backend.

The backend uses Python and the Flask library.<br>
Use a WSGI server to serve the flask app.<br>
If you have `accounts.json` and `data.json` files to load, put them in the local_data_files folder. If not, they will be automatically created by the backend.
