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
        .block-container {{
            background-color: rgba(255, 255, 255, 0.85) !important;
            color: black !important;
            padding: 2rem 3rem;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        }}
        h1, h2, h3, h4, h5, h6, label, span {{
            color: black !important;
        }}
        div.stButton > button, div.stDownloadButton > button {{
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
        div.stButton > button:hover, div.stDownloadButton > button:hover {{
            background: linear-gradient(90deg, #357ABD 0%, #4a90e2 100%) !important;
            box-shadow: 0 6px 20px rgba(53, 122, 189, 0.6) !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call background function
set_background("image.jpg")

# -------- Currency Conversion Function --------
def usd_to_inr(usd_amount):
    try:
        response = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10)
        data = response.json()
        rate = data["rates"]["INR"]
        return round(usd_amount * rate, 2)
    except Exception:
        return round(usd_amount * 83, 2)  # fallback

st.title("AI Travel Planner 🧳")

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# -------- User Inputs --------
destination = st.text_input("Enter your travel destination:")
days = st.number_input("Number of days:", min_value=1, max_value=30, value=3)
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
interests = st.text_input("Any special interests? (e.g., hiking, museums, nightlife, beaches)")

# -------- Generate Itinerary --------
if st.button("Generate Itinerary"):
    if not destination:
        st.warning("Please enter a travel destination!")
    else:
        prompt = f"""
        Plan a {days}-day {trip_type.lower()} trip to {destination}.
        Include:
        - Day-wise sightseeing, activities, accommodation ({accommodation}), transportation ({transport}), food ({food_pref})
        - Special activities: {interests if interests else 'None'}
        - Budget per person: ₹{budget_inr} INR (converted from ${budget})
        IMPORTANT:
        - Complete all {days} days.
        - Provide approximate day-wise costs and total budget.
        - Do not exceed the budget.
        - Present itinerary clearly with headings for each day.
        """

        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 1500
        }

        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
            response.raise_for_status()
            result = response.json()
            answer = result["choices"][0]["message"]["content"].strip()

            if not answer:
                st.error("Received empty itinerary. Please try again.")
            else:
                st.subheader("Your Complete Travel Plan:")
                st.text_area("Itinerary Preview", value=answer, height=400)
                
                # Generate PDF safely
                pdf_file = generate_pdf.create_pdf(answer)
                st.download_button(
                    label="Download Travel Plan as PDF",
                    data=pdf_file,
                    file_name="travel_plan.pdf",
                    mime="application/pdf"
                )
                st.write(answer)

        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
        except ValueError as e:
            st.error(f"JSON decode error: {e}\nRaw response: {response.text}")
