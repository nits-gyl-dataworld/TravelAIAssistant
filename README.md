# Travel Itinerary Generator App

![Travel Itinerary Generator](https://your-image-link.com/screenshot1.png)

## Overview

The Travel Itinerary Generator App is a tool that helps users plan their trips by generating a detailed itinerary based on their preferences. Users can specify their travel destination, dates, and interests, and the app will create a personalized travel plan. Additionally, the app includes a feature to suggest hotels within the user's budget, although this feature is mocked for demonstration purposes.

## Features

- **User Input and Preferences**: Users can enter their travel destination, start and end dates, and select their interests (e.g., art, museums, outdoor activities).
- **Dataset Integration**: The app uses a dataset to extract important features like accommodation cost for the specified destination.
- **OpenAI Integration**: The app sends a prompt to OpenAI's GPT-3.5 model to generate a structured itinerary based on user input.
- **Hotel Suggestions**: The app makes a function call (mocked for this app) to suggest hotels within the user's budget.
- **Robust Error Handling**: The app includes error handling to manage JSON decoding errors and other potential issues.

## How It Works

1. **User Input**: The user provides the travel destination, start and end dates, and selects their interests.
   
   ![User Input](https://your-image-link.com/screenshot2.png)

2. **Data Extraction**: The app reads from a CSV file to get the accommodation cost for the specified destination.
   
   ![Data Extraction](https://your-image-link.com/screenshot3.png)

3. **OpenAI Prompt**: The app constructs a prompt based on user input and sends it to OpenAI to generate an itinerary.
   
   ![OpenAI Prompt](https://your-image-link.com/screenshot4.png)

4. **Itinerary Generation**: OpenAI returns a structured JSON response with the itinerary, which the app parses and displays.
   
   ![Itinerary Generation](https://your-image-link.com/screenshot5.png)

5. **Hotel Suggestions**: Based on the accommodation cost, the app suggests hotels within the user's budget. This feature is currently mocked.
   
   ![Hotel Suggestions](https://your-image-link.com/screenshot6.png)

## Installation and Usage

To run the Travel Itinerary Generator App, follow these steps:

1. **Clone the Repository**: Clone the repository to your local machine.
   ```bash
   git clone https://github.com/yourusername/travel-itinerary-generator.git
   cd travel-itinerary-generator
2. **Set OpenAI API Key**: export OPENAI_API_KEY='your-api-key-here'
3. **Run the App**:streamlit run app.py
