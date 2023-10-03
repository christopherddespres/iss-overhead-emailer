import requests
from datetime import datetime
import smtplib
import time


MY_LAT = 42.859509  # Your latitude
MY_LONG = -71.491249  # Your longitude
gmail_smtp = "smtp.gmail.com"
gmail_email = "programtestingCD@gmail.com"
gmail_password = "vcmz komb kbpo vjuv"


def iss_overhead():
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_data = iss_response.json()

    iss_latitude = float(iss_data["iss_position"]["latitude"])
    iss_longitude = float(iss_data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def check_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True


def send_email(recipient_name, recipient_email):
    with smtplib.SMTP(gmail_smtp) as connection:
        connection.starttls()
        connection.login(user=gmail_email, password=gmail_password)
        connection.sendmail(from_addr=gmail_email, to_addrs=recipient_email,
                            msg=f"Subject:International Space Station is viewable! {recipient_name}!!\n\n"
                                f"If you look outside the International Space Station is directly above your location.")


while True:
    if iss_overhead():
        if check_dark():
            send_email("Christopher", gmail_email)
            time.sleep(43200)
    time.sleep(60)
