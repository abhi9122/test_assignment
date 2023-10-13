

# WhatsApp ChatBot
The WhatsApp ChatBot is a personalized chatbot that can be used to send messages to a WhatsApp number. 

- #### **WhatsApp Number:** +1 (415) 523-8886 (chat with code join love-brother )
- #### **Dashboard:** https://frontend-whatsappchat.vercel.app/
- #### **Django Rest API:** https://test-assignment-ofpl.onrender.com/


## Using the live project
### 1. Dashboard
- Login to the dashboard using the credentials provided.
![image](https://github.com/abhi9122/test_assignment/assets/75219190/9940464e-fdfe-43bd-ac36-83d5b124ccd6)


- Chatbot has its configuration for types like Sales, Support, etc. You can add greetings message accordangly for each type.
![image](https://github.com/abhi9122/test_assignment/assets/75219190/d6b7be7d-87b2-41b8-834d-6d22819999c4)
- Update Configuration of the chatbot. You can change the configuration of the chatbot by clicking on the Update Chatbot.
  ![image](https://github.com/abhi9122/test_assignment/assets/75219190/d4afc195-1309-4120-aa59-43c1afeb497e)
  
- Please maintain the format of the greetings message as shown in the example below, it must contains all varaibles in the same order as shown below.
    ```
    Your Yummy Cupcakes Company order of 1 dozen frosted cupcakes has shipped and should be delivered on July 10, 2019. Details: http://www.yummycupcakes.com
    ```
    - variables: 
        - Your Yummy Cupcakes Company
        - 1 dozen frosted cupcakes
        - July 10, 2019
        - http://www.yummycupcakes.com

- You can add FAQ's for the chatbot, make personalized responses for the chatbot for specific defined purpose like Sales, Customer Support, etc or edit existing one.
![image](https://github.com/abhi9122/test_assignment/assets/75219190/79bdebdf-77b4-4824-afcc-1d74436dac77)


- Records of all the messages sent to the chatbot are stored in the database and can be viewed in the dashboard and used for further agent support.
![image](https://github.com/abhi9122/test_assignment/assets/75219190/02bf60e7-56db-499b-b693-0020fe844bb7)


### 2. WhatsApp
- Send a message to the WhatsApp number provided or scan the code and message with the given code.
![image](https://github.com/abhi9122/test_assignment/assets/75219190/5bd9978e-5e72-42dd-95a9-993be13b8b89)

- The chatbot finds the best match for the incoming message and sends the appropriate response.
  ![image](https://github.com/abhi9122/test_assignment/assets/75219190/4786f8d2-495f-4ec6-96bb-71b3c8c0eecf)

- If the fuzzy score is less than 85 then the bot uses the Chatgpt3 API to generate a response to the incoming message.
![image](https://github.com/abhi9122/test_assignment/assets/75219190/dac99100-3139-49ed-b21a-ee0bd40945af)




<!-- Tech -->
## Technologies Used
- The bot is built using the `Twilio API` and the `Django`, `Django Rest FrameWork`.
- Rest API is used to create webhook to action on the incoming messages and endpoints to serve the frontend.
- The frontend is built using `ReactJS` with `Tailwind CSS`.
- `PostgreSQL` is used as the database.
- Using fuzzy matching, the bot is able to match the incoming message with the FAQ's and send the appropriate response.
- The application uses Chatgpt3 API to generate responses to the incoming messages for which the bot has no FAQ's added or the fuzzy matching fails.
- This project also has Token based authentication using `Django Rest Framework Simple JWT`.
- Fronted is deployed on Vercel Netlify and backend is deployed on Render.



## Initial Logics and Assumptions

![Untitled-2023-09-16-1518(2)](https://github.com/abhi9122/test_assignment/assets/75219190/eef47fc7-b1ac-42f9-97ed-37af48680fd7)

