
# Mind Lumina (BFRB Chatbot)

The BFRB (Body-Focused Repetitive Behaviors) chatbot is an AI-driven virtual assistant designed to help individuals manage and reduce behaviors such as hair-pulling (trichotillomania), skin-picking (dermatillomania), and nail-biting (onychophagia). Utilizing advanced **Large Language model** developed by **Google**, the chatbot provides personalized interventions, educational resources, and progress tracking to empower users on their journey toward healthier habits.


## 🔗Logo Link 
Click here to check the logo
![Logo](https://drive.google.com/file/d/175ic6PVsWvyvkCX-raetEad15VfbcW_l/view?usp=sharing)


## Problem Statement

#### Challenges in Offline Mode

1. **Behavior Tracking Issues:**
 *  Inability to automatically track behaviors using wearable devices.
   * Manual logging of BFRB episodes is hindered, leading to less accurate progress tracking.

2. **Limited Access to Educational Resources:**
  * Users cannot access the chatbot’s information library, including articles, videos, and tips.
   * Lack of educational content and practical advice during offline periods.

3. **Inconsistent Personalized Interventions:**
  * The chatbot cannot adapt responses and interventions based on real-time data.
   * Personalized treatment plans may be less effective without continuous data input.

4. **Absence of Emotional Support:**
  * No access to motivational messages and empathetic conversations.
   * Users may feel isolated and unsupported without the chatbot’s presence.

5. **Delayed Progress Tracking and Reporting:**
  * Users cannot view real-time updates and visual progress reports.
   * Inability to set or track goals effectively, potentially leading to demotivation.

6. **Disconnection from Community and Peer Support:**
 *  Users cannot connect with forums, groups, or peer mentoring programs.
   * Missed opportunities for sharing experiences and receiving support from others.

7. **Data Privacy and Security Concerns:**
  * Potential risk of data loss or synchronization issues when reconnecting to the internet.
   * Concerns about data integrity and consistency during offline periods.

8. **Limited Technical Support:**
  * Users have reduced access to immediate technical support or troubleshooting assistance.
   * Difficulties in resolving issues without online help.

9. **Restricted Mindfulness and Self-Awareness Exercises:**
 * Users cannot access guided mindfulness exercises and resources.
* Challenges in practicing mindfulness effectively without the chatbot’s guidance.

10. Reduced Adaptive Learning:

* The chatbot’s machine learning algorithms cannot update and improve without new data.
* Less effective interventions and strategies due to outdated information.

## Solution

The BFRB Chatbot project addresses the complex challenges of managing body-focused repetitive behaviors (BFRBs) through an integrated approach of technological innovation and user-centered design. By leveraging artificial intelligence and machine learning, the chatbot offers real-time support tailored to individual needs, including personalized interventions and immediate coping strategies. Users benefit from a comprehensive behavior tracking system that integrates manual logging and wearable device data, ensuring accurate progress monitoring and adaptive learning. Educational resources, such as articles and videos, provide valuable insights into BFRBs and effective management techniques. Emotionally, the chatbot delivers motivational messages and facilitates peer support through forums and mentoring programs, enhancing user engagement and resilience. Privacy and security are prioritized with encrypted data storage and user-controlled access. Future enhancements aim to incorporate advanced predictive analytics, expand language support, and integrate seamlessly with mental health platforms for comprehensive care. Ultimately, the BFRB Chatbot project aims to empower users in their journey towards healthier habits while promoting awareness and understanding of BFRBs in the broader community.







## Project Overview 
### Introduction
The BFRB (Body-Focused Repetitive Behaviors) Chatbot project is an AI-driven virtual assistant designed to help individuals manage and reduce behaviors such as hair-pulling (trichotillomania), skin-picking (dermatillomania), and nail-biting (onychophagia). This innovative tool offers comprehensive support through personalized interventions and educational resources. Users can log their behaviour manually or automatically via wearable device integration, enabling accurate progress tracking. The chatbot provides immediate coping strategies during trigger moments and fosters emotional well-being through motivational messages and empathetic conversations. Despite the challenges of offline operation, including limited real-time support and data synchronization issues, the chatbot remains a crucial aid in promoting mindfulness, self-awareness, and healthier habits.

### Key Features and Functionality

User Registration and Onboarding:

* Profile Setup: Allow users to create a profile, including information about their specific BFRBs, triggers, and goals.

* Initial Assessment: Conduct an initial assessment to understand the user's habits, triggers, and severity of their BFRBs.

Behavior Tracking:

* Manual Logging: Enable users to log instances of their BFRBs manually.
* Automated Tracking: If integrated with wearable devices or mobile sensors, the chatbot can automatically log instances based on detected patterns.
* Coping Strategies: Provide immediate suggestions for coping strategies or activities when a user feels the urge to engage in a BFRB.

Educational Resources:

* Information Library: Offer a library of articles, videos, and resources about BFRBs, their causes, and treatment options.
* Tips and Advice: Share tips for managing stress, identifying triggers, and reducing BFRBs.

Personalized Interventions:

* Adaptive Learning: Use machine learning to adapt the chatbot’s responses and interventions based on the user’s behavior and progress.
* Customized Plans: Create and adjust personalized plans to help users manage their BFRBs effectively.

Emotional Support:

* Motivational Messages: Send regular motivational messages and positive reinforcement.
* Virtual Companionship: Offer empathetic conversations to help users feel understood and supported.

Progress Tracking and Reporting:

* Visual Progress Reports: Provide visual reports showing the user’s progress over time.
* Goal Setting: Help users set and achieve short-term and long-term goals.


                     Implementation Steps

Planning and Research:

* Conduct thorough research on BFRBs and consult with mental health professionals to ensure the chatbot's interventions are effective and evidence-based.
* Define the chatbot's core functionality and user flow.



### UI/Frontend


This project is a Body-Focused Repetitive Behaviors (BFRB) Chatbot UI built with Next.js. The application provides a user-friendly interface for managing behaviors such as hair-pulling (trichotillomania), skin-picking (dermatillomania), and nail-biting (onychophagia). The chatbot offers personalized interventions, educational resources, and progress tracking to support users in reducing these behaviors.

### Table of Contents

- [Getting Started](#getting-started)
- [Routes](#routes)
- [Features](#features)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

### Getting Started

To get a local copy of the project up and running, follow these simple steps.

### Prerequisites

Make sure you have Node.js and npm installed on your machine.

- [Node.js](https://nodejs.org/)
- [npm](https://www.npmjs.com/)

### Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:swastikom/Ganak.git


##  API Reference

The API for this application has been deployed using one of the most poppular existing Python framework known as **FastAPI**. The main operation of the API involves handeling the user related requests, authentication using JWT, routes related to the chatbot along with generating report of the any particular disease found and the nearest clinic from user's address.

Let's understand each routes of the API one by one.


#### 1. Routes related to user



The routes related to user involves mainly with the operations such as **Creating** a user in the database, **Read** the current user information. **Updating** the user information and **Deleting** the user. Beside the Creating route all the other routes are protected meaning that the only authenticated user can have the access of those routes.


| Route |  Description                |
| :--------  :------------------------- |
| `POST /user/create` | Create a user and returns newly created user id. |
| `GET /user/me` | Returns the complete information of the current authenticated user. |
| `GET /user/me/update` | Updates the current authenticated user. |
| `GET /user/me/delete` | Deletes the current authenticated user. |



#### 2. User Authentication Routes



This route helps to authenticate user. It takes the email of the user along with the password and then returns a JWT token for further communication with the protected routes.


| Route |  Description                |
| :--------  :------------------------- |
| `POST /token` | Returns JWT access token after successfull authentication. |


#### 3. Password Reset Routes


Suppose a user who exists in the database has and he forgets the password. At that time this password reset routes will come to rescue the situation.

But how will that work.

Well there will be two specific routes-



| Route |  Description                |
| :--------  :------------------------- |
| `POST /password_reset/request` | This will send an OTP to the email address of the user. |
| `POST /password_reset/verify` | This will verify the OTP and allow user to set new password. |

In this way we can securely help the user to update the password in a safe and secure way.

For this API to develop MongoDB database has been used which is a non-sql database. The password and other sensitive informations are stored in the database in hash form or encrypted form. Which makes the data retrival and processing more secure for the user.


## Langchain Usage

1. Setting Up:

Import Libraries: The code starts by importing necessary libraries: os for environment variables and google.generativeai (genai) to interact with the Gemini API.

2. Function for Reusability (ask_gemini):

The code defines a function called ask_gemini that takes a prompt (the question you want to ask Gemini) as input. This function encapsulates the logic for configuring Gemini and getting a response.

3. API Key Retrieval:

Inside ask_gemini, it retrieves the API key from the environment variable named "GEMINI_API_KEY" using os.environ.get("GEMINI_API_KEY").
It checks if the API key is set. If not, it raises an error to prevent unexpected behavior.

4. Configuring Gemini:

Once the API key is retrieved, it configures the Gemini model using genai.configure(api_key=api_key). This provides access to Gemini's capabilities.

5. Model Creation and Settings (generation_config):

A dictionary named generation_config is defined. This specifies parameters for how Gemini generates responses, including:

temperature: Controls randomness in the response (1 is balanced).
top_p: Focuses generation on the most likely words (0.95 is high focus).
top_k: Considers the top k most likely words at each step (64 is a moderate value).
max_output_tokens: Limits the maximum number of words in the response (8192 is quite large).
response_mime_type: Sets the response format as plain text.
The GenerativeModel object is created using genai.GenerativeModel. It takes three arguments:

model_name: Specifies the Gemini model version ("gemini-1.5-flash" in this case).
generation_config: The dictionary defined earlier to control response generation.
safety_settings (commented out): Here you could set specific safety parameters to guide response content, but it's left out in this example.

6. Starting a Chat Session:

model.start_chat initiates a conversation with Gemini. It provides some context (history) to guide the model's understanding.

The history is a list containing two dictionaries, each representing a conversation turn:
First turn (user): The user asks "Who is swastik".
Second turn (model): Gemini provides a response asking for clarification due to the ambiguity of "Swastik".

7. Sending Your Question and Getting Response:

The prompt argument provided to the ask_gemini function is used with chat_session.send_message to send your question to the ongoing chat session with Gemini.

The response from Gemini is received as a message object, and its text is extracted and returned by the function.

Overall, the code utilizes Gemini as a large language model to answer your question based on the provided prompt and the context established in the chat history.



## Setup Instructions

### Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`GOOGLE_API_KEY` which will help us to use Google's AI related models.

`SERPER_API_KEY` which helps to use the serper library of Google to efficiently search over the internet and return things in a specific format.

`ALGORITHM` We can use specific algorithm to hash our password.

`SECRET_KEY` Secret key is a string which helps us to encrypt any string using the algorithm.

`ACCESS_TOKEN_EXPIRE_MINUTES` which specifies the time for whihc the token will expire.

`SMTP_SERVER` Specifies the SMTP server to be used for sending emails.

`SMTP_PORT` Specifies the port to be used for the SMTP server connection.

`SENDER_EMAIL` The email address from which password reset emails will be sent.

`SENDER_PASSWORD` The password or app-specific password for the sender's email account.

`MONGODB_USER` Username for connecting to the MongoDB database.

`MONGODB_PASSWORD` Password for the MongoDB user.

`MONGODB_HOST` Host address of the MongoDB server.

`MONGODB_APP_NAME` Name of the MongoDB application or database to connect to.


### Setup in Local Server

```bash
  cd frontend 
  npm run dev  

```
## Usage/Examples

### Interaction between client and chatbot
1.) User: "I feel like pulling my hair right now."

=> Chatbot: "I'm sorry to hear that you're struggling. Let's try a deep breathing exercise together. Inhale slowly for 4 seconds, hold for 4 seconds, and then exhale slowly for 4 seconds. Repeat this a few times and let me know how you feel."

2.) User: "I tried it, but I still feel the urge."

=> Chatbot: "That's okay. Sometimes it takes a bit more time. How about we try a different approach? Can you grab a stress ball or another fidget toy to keep your hands busy? Or maybe you can try doodling or writing down your feelings."
## Screenshots

![App Screenshot-1](https://drive.google.com/file/d/1yoBD7vnq6esuA3F1ZXtCvbhEKV51Dme-/view?usp=sharing)

![App Screenshot-2](https://drive.google.com/file/d/1zIP8NDu1XRC5SZrA1V8ytapcJyyqiIPE/view?usp=sharing)

![App Screenshot-3](https://drive.google.com/file/d/1QGYggRaa39xqI6a7LuSGJjMhcmSy3TdE/view?usp=sharing)

![App Screenshot-4](https://drive.google.com/file/d/1ZOUDT6_knvotfK-rn8KbqOEJQaqrXoOm/view?usp=sharing)




## Appendix

Any additional information goes here

A. Glossary of Terms

* BFRB (Body-Focused Repetitive Behaviors): A group of disorders characterized by repetitive, body-focused actions such as hair-pulling, skin-picking, and nail-biting.

* Trichotillomania: A BFRB involving recurrent, compulsive hair-pulling.

* Dermatillomania: A BFRB involving recurrent, compulsive skin-picking.

* Onychophagia: A BFRB involving recurrent, compulsive nail-biting.


## 🔗 Links

[![portfolio- Arunima Chatterjee](https://github.com/TheHappyBaloney)

[![portfolio - Swastik Dhar](https://github.com/swastikom)

[![portfolio - Suchandra Dhar](https://github.com/Suchandram)

[![portfolio - Niranjan Singh](https://github.com/niranjan65)

## Authors

- [@swastikom](https://github.com/swastikom)
- [@Suchandram](https://github.com/Suchandram)
- [@TheHappyBaloney](https://github.com/TheHappyBaloney)
- [@niranjan65](https://github.com/niranjan65)


## FAQ

#### Question 1 : How can an AI-based chatbot help with BFRBs?

Answer  : An AI-based chatbot can provide real-time support, track behaviors, offer personalized interventions, and deliver educational resources. It can help users manage their urges, identify triggers, and find healthier coping strategies.

#### Question 2 : How does the chatbot tracks my record?

Answer : The chatbot can track BFRBs through manual logging by the user and, if integrated with wearable devices, through automated monitoring of physical activity and patterns.

#### Question 3 : Is my data safe with the chatbot?
Answer : Yes, your data is securely stored and encrypted. The chatbot adheres to strict privacy regulations and ethical AI practices, ensuring your information is confidential and only used to improve your experience.

#### Question 4 :How does the chatbot provide personalized support?
Answer : The chatbot uses Large Language Model(LLM) to analyze your behaviour and progress. It adapts its responses and interventions based on your unique patterns and preferences, creating a customized experience tailored to your needs.

#### Question 5 : Are there any costs associated with using the chatbot?
Answer : As of now the chatbot is free to use. However, there may be premium features or integrations that require a subscription or one-time payment. Detailed information about any costs will be provided within the chatbot.

#### Question 6 : How is the chatbot different from traditional therapy?
Answer : The chatbot offers immediate, on-demand support and interventions, making it a convenient tool for managing BFRBs in daily life. However, it is not a replacement for traditional therapy, which provides deeper, personalized, and professional treatment.

#### Question 7 : Is the chatbot suitable for children and teenagers?
Answer : The chatbot can be used by individuals of all ages, but it is particularly designed with adult users in mind. Parents or guardians should supervise younger users and consider seeking advice from a mental health professional for age-appropriate support.

#### Question 8 : Can the chatbot provide support for other mental health issues?
Answer : While the chatbot is primarily focused on BFRBs, it can also offer general support for related issues like anxiety and stress. For more complex mental health concerns, it will recommend seeking help from a qualified professional.

#### Question 9 : Can I use the chatbot on multiple devices?
Yes, you can use the chatbot on multiple devices, such as your smartphone, tablet, and computer. Your data will sync across devices, allowing for seamless access and interaction.

#### Question 10 : Is there a limit to how often I can interact with the chatbot?
There is no limit to how often you can interact with the chatbot. It is available 24/7 to provide support whenever you need it.

