**🩺 Helfen - Conversational AI**



***Conversational AI for COVID-19 Assistance***



Helfen is a Conversational AI chatbot system developed to assist users with COVID-19 related information and services.

It integrates Dialogflow for natural language understanding and a Flask backend that connects to government APIs to provide real-time information and services.



Unlike traditional chatbots that rely on static responses, Helfen can perform real operations, such as retrieving COVID-19 statistics and downloading vaccination certificates through conversational interaction.



**Project Overview**



Many chatbots are trained on static question–answer pairs and therefore struggle to understand concepts behind user queries. This often leads to repetitive or incorrect responses.



**Helfen solves this problem by:**



* Using intent and entity recognition



* Connecting with external government APIs



* Performing real actions beyond normal chatbot responses



* Providing reliable COVID-19 information



Users can interact with the chatbot to obtain information or perform actions that are normally available only through official government portals.



**Chatbot Functionalities**



The Helfen system includes multiple chatbot modules capable of handling different COVID-19 related queries:



* Case Count – Provides current COVID-19 statistics



* Vaccination Certificate – Allows users to download their vaccination certificate



* COVID-19 Symptoms – Information about common symptoms



* Available Vaccination Slots – Displays available vaccination slots



* Protocols – Safety protocols for schools, colleges, and offices



* Preventive Measures – Guidance on how to prevent infection



* COVID-19 Guidelines – Official COVID-19 safety guidelines



* COVID-19 Symptoms Checker – Basic symptom assessment for users



**Technologies Used**



* Flask – Python micro web framework used for backend development



* Dialogflow – Used for chatbot frontend and natural language understanding



* Ngrok – Used to create a secure public URL for the local backend server



* API Setu – Government API platform used to fetch official data



* Postman – Used for API testing and validation



**Working Mechanism**



* The user sends a query to the chatbot.



* Dialogflow identifies the intent and extracts entities.



* Extracted values are stored as parameters in JSON format.



* These parameters are sent to the Flask backend through a webhook.



* The backend uses Python requests to fetch information from external APIs.



* Retrieved data is processed and returned to Dialogflow.



* Dialogflow displays the final response to the user.



**API Validation**



APIs are first tested using Postman to verify that requests are properly accepted or rejected based on validation and authentication requirements before integrating them into the system.



**Project Execution Steps**



* Start the Flask backend server written in Python.



    *python app.py*



* Once the development server generates a local URL, expose it using Ngrok.



   *ngrok http 5000*



* Copy the public Ngrok URL generated.



* Configure the Dialogflow webhook to connect with the Flask backend using this URL.



* Build and test chatbot conversations inside Dialogflow.



* The chatbot is now ready to interact with users and provide AI-powered responses.



**License**



This project is developed for educational and academic purposes.

