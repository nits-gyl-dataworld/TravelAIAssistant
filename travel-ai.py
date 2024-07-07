import streamlit as st
import json
import os
import pandas as pd
from openai import OpenAI
from datetime import datetime, timedelta
from unittest.mock import patch

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to read the travel dataset from a CSV file and extract accommodation cost
def get_accommodation_cost(destination):
  travel_df = pd.read_csv('travel_details dataset.csv')
  filtered_travel = travel_df[travel_df['Destination'] == destination]

  if filtered_travel.empty:
    return None

  # Assuming we're taking the first entry for simplicity and removing any dollar signs
  return int(filtered_travel.iloc[0]['Accommodation cost'].replace('$', '').replace(',', ''))

# Function to get external data (e.g., events, hotels)
def get_external_data(city, start_date, end_date):
  # Mocking external API response for events
  return {
    "city": city,
    "start_date": start_date,
    "end_date": end_date,
    "events": [
      {"title": "Event 1", "description": "Description of Event 1"},
      {"title": "Event 2", "description": "Description of Event 2"}
    ]
  }

# Function to get hotels data based on accommodation cost
def get_hotels_data(city, start_date, end_date, accommodation_cost):
  # Mocking hotels data
  hotels = [
    {"name": "Hotel NEANO ESCAPE ", "price_range": "$100 - $200"},
    {"name": "Hotel Amnaya Resort Nusa Dua ", "price_range": "$200 - $500"},
    {"name": "Hotel Weda Cita Resort and Spa by Mahaputra", "price_range": "$500 - $1100"},
    {"name": "Kastara Resort ", "price_range": "$1100 - $1500"},
    {"name": "Hotel Potato Head Suites & Studios  ", "price_range": "$1500 - $2600"}
  ]

  # Filter hotels based on accommodation cost
  filtered_hotels = []
  for hotel in hotels:
    price_range = hotel['price_range']
    min_price, max_price = map(int, price_range.replace('$', '').replace(' ', '').split('-'))
    if min_price <= accommodation_cost <= max_price:
      filtered_hotels.append(hotel)

  return filtered_hotels

# Streamlit app title and user input
st.title("Travel Itinerary Generator")

city = st.text_input("Enter the city you're visiting:")
start_date = st.date_input("Select the start date for your trip:", value=datetime.today())

# Set the maximum end date to 30 days after the start date
max_end_date = start_date + timedelta(days=30)

# User selects the end date of the trip
end_date = st.date_input("Select the end date for your trip:",
                         value=start_date + timedelta(days=1),  # Default to the next day
                         min_value=start_date,
                         max_value=max_end_date)
# Calculate the number of days between start_date and end_date
days = (end_date - start_date).days

art = st.checkbox("Art")
museums = st.checkbox("Museums")
outdoor = st.checkbox("Outdoor Activities")
indoor = st.checkbox("Indoor Activities")
kids_friendly = st.checkbox("Good for Kids")
young_people = st.checkbox("Good for Young People")
include_hotel = st.checkbox("Include Hotels in Itinerary")

# Generate itinerary button
if st.button("Generate Itinerary"):
  # Fetch the accommodation cost from the CSV dataset
  accommodation_cost = get_accommodation_cost(city)

  if accommodation_cost is None:
    st.error("No data found for the specified destination.")
  else:
    # Create a prompt based on user input
    prompt = f"You are a travel expert. Give me an itinerary for {city}, for {days} days, assuming each day starts at 10am and ends at 8pm with a 30-minute buffer between each activity. I like to"
    if art:
      prompt += " explore art,"
    if museums:
      prompt += " visit museums,"
    if outdoor:
      prompt += " engage in outdoor activities,"
    if indoor:
      prompt += " explore indoor activities,"
    if kids_friendly:
      prompt += " find places suitable for kids,"
    if young_people:
      prompt += " discover places suitable for young people,"

    prompt += """ Limit the length of the output JSON string to 1200 characters. Generate a structured JSON representation for the travel itinerary.

        {
            "days": [
                {
                    "day": 1,
                    "activities": [
                        {
                            "title": "Activity 1",
                            "description": "Description of Activity 1",
                            "link": "https://example.com/activity1",
                            "start_time": "10:00 AM",
                            "end_time": "12:00 PM",
                            "location": "https://maps.google.com/?q=location1"
                        },
                        {
                            "title": "Activity 2",
                            "description": "Description of Activity 2",
                            "link": "https://example.com/activity2",
                            "start_time": "02:00 PM",
                            "end_time": "04:00 PM",
                            "location": "https://maps.google.com/?q=location2"
                        },
                        ...
                    ]
                },
                ...
            ]
        }
        Ensure that each day has a 'day' field and a list of 'activities' with 'title', 'description', 'start_time', 'end_time', and 'location' fields. Keep descriptions concise.
        """

    # Call the OpenAI API without function calling
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "system", "content": "You are a travel expert."},
          {"role": "user", "content": prompt}
        ]
    )

    # Log the response from OpenAI
    # st.write("OpenAI API Response:")
    # st.write(response)

    # Process the initial response to generate the itinerary directly
    try:
      itinerary = response.choices[0].message.content.strip()
      itinerary_json = json.loads(itinerary)

      for day in itinerary_json["days"]:
        st.header(f"Day {day['day']}")
        for activity in day["activities"]:
          st.subheader(activity["title"])
          st.write(f"Description: {activity['description']}")
          try:
            st.write(f"Location: {activity['location']}")
          except KeyError:
            st.write("Location: N/A")
          st.write(f"Time: {activity['start_time']} - {activity['end_time']}")
          st.write(f"Link: {activity['link']}")
          st.write("\n")

      # Optionally include hotels in the itinerary
      if include_hotel:
        st.header("Hotels")
        st.header(f"Expected Accommodation Cost: {accommodation_cost}")
        hotels = get_hotels_data(city, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), accommodation_cost)
        st.subheader(f"Hotels Suggestions within the expected budget")
        if hotels:
          for hotel in hotels:
            st.subheader(hotel["name"])
            st.write(f"Price Range: {hotel['price_range']}")
            st.write("\n")
        else:
          st.warning("No hotels found within the specified accommodation cost range.")

    except json.JSONDecodeError as e:
      st.error(f"Failed to decode JSON response from OpenAI. Error: {e}")
      st.write("Raw JSON response:")
      st.write(itinerary)
else:
  st.info("Enter your travel details and click 'Generate Itinerary' to get started.")
