"""
Name: Your Name
CS230: Section XXX
Data: New England Airports Dataset
URL:
Description:
This program creates a simple Streamlit web application that visualizes airport data across New England states (MA, CT, RI, NH, VT, ME).
It allows filtering by state and airport type, and shows top airports by elevation and a basic airport type chart using matplotlib.
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_data():
    try:
        df = pd.read_csv("New_England_Airports.csv")
        df = df.dropna(subset=[
            "name",
            "elevation_ft",
            "iso_region",
            "type",
            "latitude_deg",
            "longitude_deg"
        ])
        return df
    except:
        st.error("Error loading the dataset. Please check the file.")
        return pd.DataFrame()
data = load_data()

# From pandas
if not data.empty:
    st.title("New England Airports Viewer")

    # [ST4] Customized page design features (sidebar and image)
    st.sidebar.header("Filter Options")
    st.st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/e/e7/Airport_icon.png",
    use_container_width=True
)

    # [ST1] Dropdown for state selection
    state = st.sidebar.selectbox("Select a state:", sorted(data["iso_region"].unique()))

    # [ST2] Dropdown for airport type
    airport_type = st.sidebar.selectbox("Select an airport type:", sorted(data["type"].unique()))

    # [DA5] Filter data by two conditions with AND
    state_mask = data["iso_region"] == state
    type_mask = data["type"] == airport_type
    filtered = data[state_mask & type_mask]

    # [DA9] Add new column using lambda function
    filtered["elevation_m"] = filtered["elevation_ft"].apply(lambda x: round(x * 0.3048, 2))

    # [DA2] Sort data
    # [DA3] Top N values
    st.subheader("Top 5 Airports by Elevation")
    top5 = filtered.sort_values(by="elevation_ft", ascending=False).head(5)
    st.write(top5[["name", "elevation_ft"]])

    # [VIZ1] Bar chart with labels and title
    st.subheader("Elevation Chart")
    fig, ax = plt.subplots()
    ax.bar(top5["name"], top5["elevation_ft"], color="skyblue")
    ax.set_ylabel("Elevation (ft)")
    ax.set_title("Top 5 Airports by Elevation")
    plt.xticks(rotation=45)
    st.pyplot(fig)


    # [PY1] Function with default value called at least once
    # [PY2] Function returns multiple values
    # [PY3] Error checking with try/except
    def calculate_stats(df, column="elevation_ft"):
        try:
            total = df[column].sum()
            count = len(df)
            if count == 0:
                return 0, 0
            return total / count, count
        except:
            return 0, 0


    # Call function with default parameter
    avg_ft, count_ft = calculate_stats(filtered)

    # Call function with custom parameter
    avg_m, count_m = calculate_stats(filtered, column="elevation_m")

    # Display results
    st.write(f"Average Elevation for {airport_type} airports in {state}: {avg_ft:.2f} ft across {count_ft} airports.")
    st.write(f"Average Elevation for {airport_type} airports in {state}: {avg_m:.2f} m across {count_m} airports.")

    # [PY4] List comprehension
    airport_names = [name for name in filtered["name"] if "airport" in name.lower()]
    st.write(f"Airports with 'airport' in the name: {len(airport_names)}")

    # [PY5] Dictionary access of keys/values
    counts_by_type = {typ: len(data[data["type"] == typ]) for typ in data["type"].unique()}
    st.write("Airport Type Counts:", counts_by_type)

    # [MAP] Streamlit basic map with detailed hover simulated by table
    st.subheader("Airport Locations on Map")
    map_data = filtered.rename(columns={"latitude_deg": "latitude", "longitude_deg": "longitude"})
    st.map(map_data[["latitude", "longitude"]])

    # [VIZ2] Table for map detail (simulated hover info)
    # [ST3] DataFrame output/table as widget
    st.write("Detailed Airport Info (Simulated Hover)")
    st.dataframe(map_data[["name", "elevation_ft", "latitude", "longitude"]])

    # Show calculated elevation in meters (from lambda)
    st.subheader("Elevation in Meters (Calculated with Lambda)")
    st.write(filtered[["name", "elevation_ft", "elevation_m"]])
