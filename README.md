                                                   AI TRAVEL PLANNER

An AI-powered web application that generates personalized travel itineraries based on user preferences 
such as destination, budget, number of days, and travel style. 
The system uses NLP-based AI models to create intelligent, budget-aware, day-wise travel plans and 
provides them as on-screen output and downloadable PDF files.

Features:
- Personalized travel itinerary generation
- Budget-aware planning with day-wise cost estimation
- Real-time currency conversion (USD → INR)
- AI-powered itinerary generation using NLP models
- Downloadable travel plan in PDF format
- Simple and user-friendly web interface
- Cloud-deployed and accessible from anywhere

The project follows a layered architecture:

- User Interface Layer (Streamlit UI)
- Application Layer (Input processing & prompt construction)
- AI Processing Layer (NLP-based itinerary generation)
- External Services Layer (Currency conversion API)
- Output Layer (PDF generation & display)
- Deployment Layer (Streamlit Cloud)

Tools & Technologies Used
- Programming Language: Python
- Frontend: Streamlit
- Backend: Python (Streamlit backend logic)
- Artificial Intelligence / NLP: OpenRouter API
- GPT-based conversational AI models

Libraries:
- streamlit: Web application framework
- requests: API communication
- fpdf: PDF generation
- io(BytesIO): In-memory file handling
- textwrap: Text formatting
- python-dotenv: Environment variable management

Development & Deployment Tools:
- Visual Studio Code (IDE)
- Git & GitHub (Version control)
- Streamlit Cloud (Deployment)
