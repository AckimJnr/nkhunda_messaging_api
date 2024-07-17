# NKHUNDA MESSAGING API
⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⡈⠛⢿⣿⣶⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀
⠀⠸⢿⣿⣶⣾⣿⣿⣿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣴⣾⠇⠀
⠀⠀⢤⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⣠⣤⣴⣶⣶⣾⣿⡿⠟⠋⣁⡀⠀
⠀⠀⠘⢉⣩⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣟⠛⠛⠁⠀
⠀⠀⠀⠈⠻⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿⣟⠿⣿⠃⠀⠀
⠀⠀⠀⠀⠀⠈⠻⠟⣿⣿⣿⣿⣿⣿⣿⣿⣄⣿⣿⣿⣿⣿⣿⣿⣿⡷⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⣉⣽⣿⣿⣿⣿⡿⢻⣿⣿⣿⢿⣿⠎⠉⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣤⣴⣶⣾⣿⣿⣿⣿⣿⣿⣿⣦⡀⠈⠉⠉⠁⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣉⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠙⠋⣽⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⠿⠋⣸⣿⡟⢸⣿⣿⠉⣿⣿⡘⢿⡷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠀⢸⣿⡏⠀⠸⠿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
## Description
- This api was developed solery to speed up development process of systems that may require messaging features
- Organisation once they register their api in NKHUNDA recieve an api key that they can use to send and recieve messages on the NKHUNDA API Queue

## Setup instructions
1. Clone the project in on your local machine
2. Create a python Virtual environment and activate it
3. Install the requirement from the requirements.txt file
4. Navigate to api/vi
    - Inside the folder run the worker for the queue using `rq worker nkhunda_message_queue`
    - Run the main app using `uvicorn main:app --reload`
    - Open the base url open */docs* to access the swagger documentantion