import logging
import os

import requests
import streamlit as st

logging.basicConfig(filename="app.log", filemode="w", level=logging.DEBUG)

REQUESTS_URL = os.environ["REQUESTS_URL"]
# A session to be used for all HTTP requests
session = requests.Session()


# Streamlit App
st.title("Set up an activity and test it out!")

st.text_input("Enter your 10 digit phone number", key="user_phone", placeholder="3334445555")
if st.button("Submit Phone"):
    st.write("Adding user to db...")

    logging.debug(f"adding user with phone {st.session_state.user_phone}")
    user = requests.post(
        url=f"{REQUESTS_URL}/users",
        data={
            "phone": st.session_state.user_phone,
            "active": True,
            "notification_method": "Twilio",
        },
    )
    logging.debug("user added\n", user)
    st.write("User Submitted!")


st.text_input("Give your activity a name", key="activity_name", placeholder="Mountain Biking")

with st.container():
    col1, col2, col3 = st.columns(3)
    col1.write(
        """
    #### Time
    Enter the the hour of day [0 - 23]
    """
    )
    col2.text_input("Earliest hour to start at", key="time_min_val", placeholder="9 - 9:00 AM")
    col3.text_input("Latest hour to end at", key="time_max_val", placeholder="16 - 4:00")

    col1, col2, col3 = st.columns(3)
    col1.write(
        """
    #### Temperature
    Enter temperatures in degress
    """
    )
    col2.text_input("Minimum temp", key="temp_min_val", placeholder="65")
    col3.text_input("Maximum temp", key="temp_max_val", placeholder="90")

    col1, col2, col3 = st.columns(3)
    col1.write(
        """
    #### Wind Speed
    Enter wind speed in mph
    """
    )
    col2.text_input("Minimum wind speed", key="wind_min_val", placeholder="0")
    col3.text_input("Maximum wind speed", key="wind_max_val", placeholder="10")

    col1, col2, col3 = st.columns(3)
    col1.write(
        """
    #### Cloud Coverage
    Enter a percentage [0 - 100]
    """
    )
    col2.text_input("Minimum cloud coverage", key="clouds_min_val", placeholder="0")
    col3.text_input("Maximum cloud coverage", key="clouds_max_val", placeholder="25")

    col1, col2, col3 = st.columns(3)
    col1.write(
        """
    #### UV Index
    Enter UV Index [0 - 12]
    """
    )
    col2.text_input("Minimum UV index", key="uv_min_val", placeholder="6")
    col3.text_input("Maximum UV index", key="uv_max_val", placeholder="10")

    col1, col2, col3 = st.columns(3)
    col1.write(
        """
    #### Precipitation
    Enter a percentage for the chance of precipitation
    """
    )
    col2.text_input("Minimum chance of precipitation", key="precip_min_val", placeholder="0")
    col3.text_input("Maximum chance of precipitation", key="precip_max_val", placeholder="0")

    if st.button("Create Activity"):
        st.write("Adding activity to db...")

        activity = session.post(
            url=f"{REQUESTS_URL}/users/{user.id}/activities",
            data={
                "name": st.session_state.activity_name,
                "active": 1,
            },
        )

        time_cosntraint = session.post(
            url=f"{REQUESTS_URL}/activities/{activity.id}/constraint",
            data={
                "metric": "Time",
                "miminum_value": st.session_state.time_min_val,
                "maximum_value": st.session_state.time_max_val,
            },
        )

        if st.session_state.temp_min_val is not None or st.session_state.temp_max_val is not None:
            temp_cosntraint = session.post(
                url=f"{REQUESTS_URL}/activities/{activity.id}/constraint",
                data={
                    "metric": "Temperature",
                    "miminum_value": st.session_state.temp_min_val,
                    "maximum_value": st.session_state.temp_max_val,
                },
            )

        if st.session_state.wind_min_val is not None or st.session_state.wind_max_val is not None:
            wind_cosntraint = session.post(
                url=f"{REQUESTS_URL}/activities/{activity.id}/constraint",
                data={
                    "metric": "Wind Speed",
                    "miminum_value": st.session_state.wind_min_val,
                    "maximum_value": st.session_state.wind_max_val,
                },
            )

        if st.session_state.clouds_min_val is not None or st.session_state.clouds_max_val is not None:
            clouds_cosntraint = session.post(
                url=f"{REQUESTS_URL}/activities/{activity.id}/constraint",
                data={
                    "metric": "Cloud Coverage",
                    "miminum_value": st.session_state.clouds_min_val,
                    "maximum_value": st.session_state.clouds_max_val,
                },
            )

        if st.session_state.uv_min_val is not None or st.session_state.uv_max_val is not None:
            uv_cosntraint = session.post(
                url=f"{REQUESTS_URL}/activities/{activity.id}/constraint",
                data={
                    "metric": "UV Index",
                    "miminum_value": st.session_state.uv_min_val,
                    "maximum_value": st.session_state.uv_max_val,
                },
            )

        if st.session_state.precip_min_val is not None or st.session_state.precip_max_val is not None:
            precip_cosntraint = session.post(
                url=f"{REQUESTS_URL}/activities/{activity.id}/constraint",
                data={
                    "metric": "Precipitation",
                    "miminum_value": st.session_state.precip_min_val,
                    "maximum_value": st.session_state.precip_max_val,
                },
            )

        st.write("Activity Submitted!")

st.write("# Check the weather")

if st.button("Check weather"):
    st.write(f"Based on today's weather forecast, it is a perfect day for {st.session_name.activity_name}")
