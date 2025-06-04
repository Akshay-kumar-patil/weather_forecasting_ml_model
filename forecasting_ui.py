import streamlit as st
import pickle
import requests

# reading model.pickle
with open("rain_model.pkl","rb") as f:
    model=pickle.load(f)


# weather api initiating
api_key ='e3ebc63fa8d066ecd56de1c8cbe220a0'
base_url='https://api.openweathermap.org/data/2.5/'

# fetching data through api
def get_data(city):
    url = f"{base_url}weather?q={city}&appid={api_key}&units=metric"
    response=requests.get(url)
    data = response.json()
    
    if response.status_code !=200:
        return None

    weather_data=  {
      'city' : data['name'],
      'feels_like': round(data['main']['feels_like']),
      'Temperature': round(data['main']['temp']),
      'Humidity' : round(data['main']['humidity']),
      'Wind_Speed' : data['wind']['speed'],
      'Cloud_Cover' : data['clouds']['all'],
      'Pressure' : data['main']['pressure'],
      'country' : data['sys']['country'],
    }

    return weather_data

#straimlit UI
st.title("🌦️ Weather Forecast and Rain Prediction")

city = st.text_input("Enter city name")

st.button("Analyze")

if city:
    data=get_data(city)

    if data:
        st.subheader(f"📍Weather in {data['city']},{data['country']} ")
        st.metric("🌡️ Temperature (°C)",data['Temperature'])
        st.metric("🥵 Feels Like (°C)",data['feels_like'])
        st.metric("💧 Humidity (%)", data['Humidity'])
        st.metric("🌬️ Wind Speed (m/s)", data['Wind_Speed'])
        st.metric("☁️ Cloud Cover (%)", data['Cloud_Cover'])
        st.metric("📈 Pressure (hPa)", data['Pressure'])

        features=[[
            data['Temperature'],
            data['Humidity'],
            data['Wind_Speed'],
            data['Cloud_Cover'],
            data['Pressure'],
        ]]

        prediction=model.predict(features)[0]


        st.markdown("------")
        if prediction == 1:
            st.success("🌧️ Rain is Likely. Carry an Umbrella!...")
        else:
            st.info("☀️ No rain predicted. Have a great day!...")
    else:
        st.error("❌ City not found or API error.")