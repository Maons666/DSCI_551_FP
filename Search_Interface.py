import streamlit as st
import requests
import json
import math
import folium
import base64
from PIL import Image
from io import BytesIO
from streamlit_folium import st_folium
from folium.plugins import MousePosition
from datetime import datetime, date

DATABASE_URLS = {
    0: "https://lost-items-f914d-default-rtdb.firebaseio.com/items",
    1: "https://found-items-7dec3-default-rtdb.firebaseio.com/items",
    2: "https://resolved-items-default-rtdb.firebaseio.com/items"
}

# DATABASE_URLS = {
#     0: "https://dsci551-hw1-db1-6491a-default-rtdb.firebaseio.com/items",
#     1: "https://dsci551-hw1-db2-54c48-default-rtdb.firebaseio.com/items",
#     2: "https://dsci-551-xinyu-wang-default-rtdb.asia-southeast1.firebasedatabase.app/items"
# }

NOIMAGE = "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"

def calculate_square_bounds(lat, lon, side_meters=200):
    meters_per_degree_lat = 111000 
    delta_lat = (side_meters / 2) / meters_per_degree_lat
    delta_lon = (side_meters / 2) / (meters_per_degree_lat * math.cos(math.radians(lat)))
    min_lat = lat - delta_lat
    max_lat = lat + delta_lat
    min_lon = lon - delta_lon
    max_lon = lon + delta_lon
    
    return min_lat, max_lat, min_lon, max_lon

def handle_Empty(text):
    if text == "":
        return "N/A"
    else:
        return text

def SearchPage():
    st.title('Search Engine')
    filter_select = "ID"
    filter_select = st.radio("Which filter would you like to choose?", ('ID', 'Type', 'Date', 'Location'))

    if filter_select == 'ID':
        item_id = st.text_input("Item ID:", key="item_id")
        if item_id.startswith("L"):
            index = 0
        else:
            index = 1
        search_url = {"url": f"{DATABASE_URLS[index]}/{item_id}.json?", "id": item_id}
    elif filter_select == 'Type':
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

        item_Cate = st.selectbox("Item Category", item_type_options, key = "Item_type")
        if item_Cate == 'Other':
            item_Cate = st.text_input("Specify item type...")
        search_param = f'.json?orderBy="item_type"&equalTo="{item_Cate}"'
        search_url = []
        for key, url in DATABASE_URLS.items():
            search_url.append(f"{url}{search_param}")

    elif filter_select == 'Date':
        date_start = st.date_input("Start date")
        date_end = st.date_input("End date")#, value = date.today()
        date_start_inclusive = datetime.combine(date_start, datetime.min.time()).timestamp()
        date_end_inclusive = datetime.combine(date_end, datetime.max.time()).timestamp()
        search_param = f'.json?orderBy="date"&startAt={date_start_inclusive}&endAt={date_end_inclusive}'
        search_url = []
        for key, url in DATABASE_URLS.items():
            search_url.append(f"{url}{search_param}")

    elif filter_select == "Location":
        st.write(f"Click on the location for a search center...")
        m = folium.Map(location=[34.02237401218679, -118.28523627163219], zoom_start=16)
        formatter = "function(num) {return L.Util.formatNum(num, 5);};"
        MousePosition(position="bottomright", separator=" | ", lng_first=False,
                    num_digits=20, prefix="Coordinates:", lat_formatter=formatter, lng_formatter=formatter).add_to(m)
        map_result = st_folium(m, width=725, height=525)

        # Manual coordinate entry after map location identification
        if map_result["last_clicked"]:
            lat = map_result["last_clicked"]["lat"]
            lon = map_result["last_clicked"]["lng"]
            st.write(f"Coordinate selected: {lat}, {lon}")
        else:
            lat = 0
            lon = 0
            st.write("Waiting for location selection...")
        search_url = {}
        search_url["bound"] = calculate_square_bounds(lat, lon)
        search_url["urls"] = []
        search_param = f'.json?orderBy="latitude"&startAt={search_url["bound"][0]}&endAt={search_url["bound"][1]}'
        for key, url in DATABASE_URLS.items():
            search_url["urls"].append(f"{url}{search_param}")

# --------------------------------------------------------------------- #
    search_button = st.button('Search')
    mark_button = st.button('Mark as resolved!')

    if search_button and filter_select == "ID":
        response = requests.get(search_url["url"])
        results = response.json()
        st.session_state.mark["data"] = response.json()
        st.session_state.mark["data_id"] = search_url["id"]
        st.session_state.mark["dataurl"] = search_url["url"]
        st.markdown("---")
        if results:
            with st.container():
                col1, col2 = st.columns([1, 2])
                if results["image"] == "":
                    base64_string = NOIMAGE
                else:
                    base64_string = results["image"]
                with col1:
                    image_bytes = base64.b64decode(base64_string)
                    image_data = BytesIO(image_bytes)
                    st.image(image_data)

                    # if 'search_results' not in st.session_state:
                    #     st.session_state.search_results = results  # Initialize if not already

                    # if 'search_results' in st.session_state and st.session_state.search_results is not None:
                    #     if st.button("Mark as resolved!"):
                    #         st.write("Button pressed")  # Debug statement
                    #         st.session_state.search_results["completed"] = True
                    # if st.button("Mark as resolved!"):
                    #     results["completed"] = True
                    #     responseD = requests.delete(search_url["url"])
                    #     dataurl = DATABASE_URLS[2]
                    #     dataid = search_url["id"]
                    #     st.write(results)
                    #     st.write(f"{dataurl}/{dataid}.json")
                    #     responseA = requests.patch(f"{dataurl}/{dataid}.json", data=json.dumps(st.session_state.search_results))
                    #     st.success("Congratulations! Item has been resolved!")



                with col2:
                    st.write(f"Status:         {handle_Empty(results.get('status'))}")
                    st.write(f"Type:           {handle_Empty(results.get('item_type'))}")
                    st.write(f"Color:          {handle_Empty(results.get('color'))}")
                    if results["date"]:
                        date_from_stamp = datetime.fromtimestamp(results["date"]).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        date_from_stamp = "N/A"
                    st.write(f"Date submitted：{date_from_stamp}")
                    st.write(f"Email:          {handle_Empty(results.get('email'))}")
                    st.write(f"Phone:          {handle_Empty(results.get('phone'))}")
                    st.write(f"Description: {handle_Empty(results.get('description'))}")
                st.markdown("---")
        else:
            st.write("No such ID found in database...")
    elif search_button and isinstance(search_url, list) and not filter_select == "Location":
        results = {}
        for url in search_url:
            response = requests.get(url)
            results.update(response.json() or {})
        st.markdown("---")
        if results:
            for resultKey, result in results.items(): 
                with st.container():
                    col1, col2 = st.columns([1, 2])
                    if result["image"] == "":
                        base64_string = NOIMAGE
                    else:
                        base64_string = result["image"]
                    with col1:
                        image_bytes = base64.b64decode(base64_string)
                        image_data = BytesIO(image_bytes)
                        st.image(image_data)
                    with col2:
                        st.write(f"Status:         {handle_Empty(result.get('status'))}")
                        st.write(f"Type:           {handle_Empty(result.get('item_type'))}")
                        st.write(f"Color:          {handle_Empty(result.get('color'))}")
                        if result["date"]:
                            date_from_stamp = datetime.fromtimestamp(result["date"]).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            date_from_stamp = "N/A"
                        st.write(f"Date submitted：{date_from_stamp}")
                        st.write(f"Email:          {handle_Empty(result.get('email'))}")
                        st.write(f"Phone:          {handle_Empty(result.get('phone'))}")
                        st.write(f"Description: {handle_Empty(result.get('description'))}")
                    st.markdown("---")
    elif search_button and isinstance(search_url, dict) and filter_select == "Location":
        results = {}
        for url in search_url["urls"]:
            response = requests.get(url)
            results.update(response.json() or {})
        st.markdown("---")
        if results:
            for resultKey, result in results.items(): 
                if result['longitude'] >= search_url["bound"][2] and\
                result['longitude'] <= search_url["bound"][3]:
                    with st.container():
                        col1, col2 = st.columns([1, 2])
                        if result["image"] == "":
                            base64_string = NOIMAGE
                        else:
                            base64_string = result["image"]
                        with col1:
                            image_bytes = base64.b64decode(base64_string)
                            image_data = BytesIO(image_bytes)
                            st.image(image_data)
                        with col2:
                            st.write(f"Status:         {handle_Empty(result.get('status'))}")
                            st.write(f"Type:           {handle_Empty(result.get('item_type'))}")
                            st.write(f"Color:          {handle_Empty(result.get('color'))}")
                            if result["date"]:
                                date_from_stamp = datetime.fromtimestamp(result["date"]).strftime('%Y-%m-%d %H:%M:%S')
                            else:
                                date_from_stamp = "N/A"
                            st.write(f"Date submitted：{date_from_stamp}")
                            st.write(f"Email:          {handle_Empty(result.get('email'))}")
                            st.write(f"Phone:          {handle_Empty(result.get('phone'))}")
                            st.write(f"Description: {handle_Empty(result.get('description'))}")
                        st.markdown("---")
    if mark_button:
        if st.session_state.mark:
            st.session_state.mark["data"]["completed"] = True
            responseD = requests.delete(st.session_state.mark["dataurl"])
            markurl = f"{DATABASE_URLS[2]}/{st.session_state.mark['data_id']}.json"
            responseA = requests.patch(markurl, data=json.dumps(st.session_state.mark["data"]))
            st.success("Congratulations! Item has been resolved!")
            st.session_state.mark = {}
        else:
            st.write("Please search by ID first!")



# if __name__ == "__main__":
#     SearchPage()