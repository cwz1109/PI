import smbus2
import bme280
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# BME280 sensor address (default address)
address = 0x76

# Initialize I2C bus
bus = smbus2.SMBus(1)

# Load calibration parameters
calibration_params = bme280.load_calibration_params(bus, address)


def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32


def send_email(subject, body, sender_email, receiver_email, password):
    # Set up the SMTP server using SSL
    server = smtplib.SMTP_SSL('mail.messagingengine.com', 465)

    # Log in to the email server
    server.login(sender_email, password)

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the text to the email
    msg.attach(MIMEText(body, 'plain'))

    # Send the email and close the connection
    server.send_message(msg)
    server.quit()


# User credentials and recipient's email
sender_email = "christor@fastmail.cn"
receiver_email = "weize.chen@ucdconnect.ie"
password = "qwtma9fuxvzpws67"

# Collect and send the data once
try:
    data = bme280.sample(bus, address, calibration_params)
    temperature_celsius = data.temperature
    pressure = data.pressure
    humidity = data.humidity
    temperature_fahrenheit = celsius_to_fahrenheit(temperature_celsius)

    # Prepare email content
    subject = "BME280 Sensor Readings"
    body = f"Temperature: {temperature_celsius:.2f} °C, {temperature_fahrenheit:.2f} °F\nPressure: {pressure:.2f} hPa"

    # Send an email with the data
    send_email(subject, body, sender_email, receiver_email, password)

    print("Email sent with sensor data.")

except Exception as e:
    print('An unexpected error occurred:', str(e))

quit()