import streamlit as st
import requests
import generate_pdf
from dotenv import load_dotenv
import os

import base64
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="🧳",
    layout="centered"
)

# -------- Background Image Function --------
def set_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        /* Make main container slightly transparent for readability */
        .block-container {{
            background-color: rgba(255, 255, 255, 0.85) !important;
            color: black !important;
            padding: 2rem 3rem;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        }}

        /* Headings and text color */
        h1, h2, h3, h4, h5, h6, label, span {{
            color: black !important;
        }}

         /* Generate Itinerary button */
    div.stButton > button {{
        color: white !important;
        background: linear-gradient(90deg, #4a90e2 0%, #357ABD 100%) !important;
        border: none !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(53, 122, 189, 0.4) !important;
        transition: background 0.3s ease, box-shadow 0.3s ease !important;
        cursor: pointer;
    }}

    div.stButton > button:hover {{
        background: linear-gradient(90deg, #357ABD 0%, #4a90e2 100%) !important;
        box-shadow: 0 6px 20px rgba(53, 122, 189, 0.6) !important;
    }}

    /* Download PDF button */
    div.stDownloadButton > button {{
        color: white !important;
        background: linear-gradient(90deg, #4a90e2 0%, #357ABD 100%) !important;
        border: none !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(53, 122, 189, 0.4) !important;
        transition: background 0.3s ease, box-shadow 0.3s ease !important;
        cursor: pointer;
    }}

    div.stDownloadButton > button:hover {{
        background: linear-gradient(90deg, #357ABD 0%, #4a90e2 100%) !important;
        box-shadow: 0 6px 20px rgba(53, 122, 189, 0.6) !important;
    }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function with your image
set_background("image.jpg")

# -------- Currency Conversion Function --------
def usd_to_inr(usd_amount):
    try:
        response = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10)
        data = response.json()
        rate = data["rates"]["INR"]
        return round(usd_amount * rate, 2)
    except Exception:
        return round(usd_amount * 83, 2)  # fallback rate
st.title("AI Travel Planner 🧳")


load_dotenv()  # MUST be before os.getenv

API_KEY = os.getenv("OPENROUTER_API_KEY")

# Put your OpenRouter API key here


API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

destination = st.text_input("Enter your travel destination:")
days = st.number_input("Number of days:", min_value=1, max_value=30, value=3)
# 🔹 Add budget input here
budget = st.number_input("Approximate budget in USD per person:", min_value=50, max_value=10000, value=500)
budget_inr = usd_to_inr(budget)
st.write(f"💰 Budget in INR: ₹{budget_inr}")

trip_type = st.selectbox(
    "Select your travel style:",
    ["Adventure", "Relaxation", "Cultural", "Foodie", "Shopping", "Mixed"]
)
accommodation = st.selectbox(
    "Preferred accommodation type:",
    ["Hotel", "Hostel", "Airbnb", "Guesthouse", "Luxury"]
)

transport = st.selectbox(
    "Preferred transportation mode:",
    ["Public transport", "Car rental", "Bike", "Walking", "Mixed"]
)

food_pref = st.selectbox(
    "Food preference:",
    ["Local cuisine", "Vegetarian", "Vegan", "Seafood", "No preference"]
)
interests = st.text_input(
    "Any special interests? (e.g., hiking, museums, nightlife, beaches)"
)

if st.button("Generate Itinerary"):
    if not destination:
        st.warning("Please enter a travel destination!")
    else:
        # Prepare the prompt
        prompt = f"""
        Plan a {days}-days {trip_type.lower()} trip to {destination}.
        Include:
        - Day-wise sightseeing and activities
        - Accommodation ({accommodation})
        - Transportation tips ({transport})
        - Food suggestions ({food_pref})
        - Special activities related to interests: {interests}
        - Approximate budget per person: ₹{budget_inr} INR (converted from ${budget})
        IMPORTANT:
        - Complete ALL {days} days
        - Do not stop mid-sentence
        - Finish the itinerary fully

        Make the itinerary easy to read, practical, and detailed.
        """

        # JSON payload for OpenRouter (GPT-style)
        payload = {
            "model": "gpt-4o-mini",  # fast, free model available via OpenRouter
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1500
        }

        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
            
            if response.status_code == 200:
                result = response.json()
                answer = result["choices"][0]["message"]["content"]
                st.subheader("Your Complete Travel Plan:")
                st.text_area("Itinerary Preview", value=answer, height=400)
                # Download button
                pdf_file = generate_pdf.create_pdf(answer)
                st.download_button(
                    label="Download Travel Plan as PDF",
                    data=pdf_file,
                    file_name="travel_plan.pdf",
                    mime="application/pdf"
                    )
                st.write(answer)
            else:
                st.error(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
        except ValueError as e:
            st.error(f"JSON decode error: {e}\nRaw response: {response.text}")
