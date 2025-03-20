import streamlit as st
import pandas as pd
import pandas as pd
import requests
import json
from datetime import datetime

def get_listings():
    url = "https://realtor-com4.p.rapidapi.com/properties/list"
    headers = {'Content-Type': 'application/json', 'x-rapidapi-host': 'realtor-com4.p.rapidapi.com', 'x-rapidapi-key': '0659fec61amshef4693f4e95e24bp1666c2jsnc00727806bae'}
    home_data = {
    "query": {
        "status": [
        "for_sale"
        ],
        "city": "Las Vegas", "state_code": "NV"
    },
    "limit": 10,
    "offset": 0,
    "sort": {
        "direction": "asc",
        "field": "list_date"
    }
    }

    response = requests.post(url, headers=headers, json=home_data)

    # print(response.json()) #.json will show actual property data requested from the API

    property_list = response.json()['data']['home_search']['properties'] 

    df = pd.DataFrame(property_list)

    clean_data = []

    for index, row in df.iterrows():
        branding_name = row['branding'][0]['name']
        line = row['location']['address']['line']
        city = row['location']['address']['city']
        state = row['location']['address']['state_code']
        zip_code = row['location']['address']['postal_code']

        full_address = f"{line}, {city}, {state} {zip_code}"
        price = row['list_price']
        list_date = row["list_date"]

        if line[0].isdigit():
            listing_date = datetime.strptime(list_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            formatted_list_date = listing_date.strftime("%Y-%m-%d")
            days_on_market = (datetime.today() - listing_date).days

            clean_data.append({
                "Agent/Company": branding_name, 
                "Property Address": full_address, 
                "List Price": price, 
                "Listing Date": formatted_list_date,
                "Days on Market": days_on_market
            })
            
    clean_df = pd.DataFrame(clean_data)
    clean_df.to_csv("clean_realtor_data.csv", index=False)

    return clean_df

st.title("Las Vegas Listings")
st.markdown("Click the button below to pull real estate listings in Las Vegas, NV.")

if st.button("Get Listings"):
    clean_df = get_listings()

    if clean_df.empty:
        st.warning("No listings found or something went wrong.")
    else:
        st.success("Listings successfully pulled for Las Vegas, NV")
        st.dataframe(clean_df)

        # Download button
        csv = clean_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="las_vegas_listings.csv",
            mime="text/csv"
        )