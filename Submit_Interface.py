import base64
import streamlit as st
import requests
import json
import folium
import random
from streamlit_folium import st_folium
from folium.plugins import MousePosition
from PIL import Image
from datetime import datetime, date



DATABASE_URLS = {
    0: "https://lost-items-f914d-default-rtdb.firebaseio.com/items",
    1: "https://found-items-7dec3-default-rtdb.firebaseio.com/items",
    2: "https://resolved-items-default-rtdb.firebaseio.com/items"
    }

def randomChar(l):
    dicR = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    word = ""
    for i in range(l):
        word = word + random.choice(dicR)
    return word

def generate_id(status):
    # Determin prefix
    prefix = 'L' if status.lower() == 'lost' else 'F'
    ID_body = randomChar(10)
    itemID = f"{prefix}{ID_body}"
    return itemID

def submit_pause(seconds_limit):
    if 'last_submit_time' in st.session_state:
        elapsed_time = datetime.now() - st.session_state['last_submit_time']
        return elapsed_time.total_seconds() < seconds_limit
    else:
        return False

def SubmitPage():
    st.title('Submit Item Info')

    # Status selection
    status = "Lost"
    status = st.radio("Is this a lost or Found Item?", ('Lost', 'Found'))

    # Item type selection
    item_type_options = [
    'Electronic Devices', 
    'Keys', 
    'Wallets and Identification Cards', 
    'Textbooks and Notebooks', 
    'Clothing', 
    'Eyeglasses and Sunglasses', 
    'Water Bottles and Lunch Boxes', 
    'Backpacks and Bags', 
    'Sporting Equipment', 
    'Umbrellas',
    'Other'
    ]

    item_Cate = st.selectbox("Item Category", item_type_options)
    if item_Cate == 'Other':
        item_Cate = st.text_input("Specify item type...")

    # Color selection
    color_options = ['Red', 'Green', 'Blue', 'Yellow', 'Black', 'White', 'Other']
    color = st.selectbox("Color", color_options)
    if color == 'Other':
        color = st.text_input("Specify color...")

    # upload image of the item
    
    uploaded_file = st.file_uploader("Choose an image of the item. JPG and PNG format only.", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.write("Image Uploaded Successfully!")
        
        # Display the image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)

        # Read the image as bytes
        image_bytes = uploaded_file.read()
        # Encode these bytes to Base64
        base64_encoded = base64.b64encode(image_bytes)
        # Convert to string for easier handling
        item_image_str = base64_encoded.decode('utf-8')
    else:
        item_image_str = ""

    # Description input
    description = st.text_area("Description")

    # Date input
    today = date.today()
    date_input = st.date_input(f"When did you {status.lower()} it?", today)
    datestamp = datetime.combine(date_input, datetime.now().time()).timestamp()

    # location input
    st.write(f"Click on the location where the item is {status}")
    m = folium.Map(location=[34.02237401218679, -118.28523627163219], zoom_start=16)
    formatter = "function(num) {return L.Util.formatNum(num, 5);};"
    MousePosition(position="bottomright", separator=" | ", lng_first=False,
                num_digits=20, prefix="Coordinates:", lat_formatter=formatter, lng_formatter=formatter).add_to(m)
    result = st_folium(m, width=725, height=525)

    # Manual coordinate entry after map location identification
    if result["last_clicked"]:
        lat = result["last_clicked"]["lat"]
        lon = result["last_clicked"]["lng"]
        st.write(f"Coordinate selected: {lat}, {lon}")
    else:
        lat = 0
        lon = 0
        st.write("Waiting for location selection...")
        st.write("Will not record location if not selected.")

    # Contact information
    phone = st.text_input("Phone Number")
    email = st.text_input("Email Address")

    # Submit
    if submit_pause(10):  # 10 seconds wait time
        st.write("Please wait for 10 seconds after submitting an item to submit another.")
    else:
        if st.button('Submit'):
            # Assuming a function to handle the submission process
            # For demonstration, we'll just display the entered information
            # json structure adjustment needed
            item_id = generate_id(status)
            itemJson = {
                "status": status,
                "item_type": item_Cate,
                "color": color,
                "image": item_image_str,
                "description": description,
                "date": datestamp,
                "latitude": lat, "longitude": lon,
                "phone": phone, "email": email, 
                "completed": False
            }
            # Select database based on the ID
            if item_id.startswith("L"):
                url = DATABASE_URLS[0]
            else:
                url = DATABASE_URLS[1]
            itemJson_serialized = json.dumps(itemJson)
            response = requests.patch(f"{url}/{item_id}.json", data=itemJson_serialized)
            st.session_state['last_submit_time'] = datetime.now()
            st.success("Item submitted successfully!")
            st.success("Please remember the Item ID of the item you just submited!")
            st.success(f"Item ID: {item_id}")
            
# if __name__ == '__main__':
#     SubmitPage()
