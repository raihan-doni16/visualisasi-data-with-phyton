import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import calendar


sns.set(style="white")

# set data keseluruhan
def create_data_all(df):
    month_names = {i: calendar.month_name[i] for i in range(1, 13)}
    dataset_all = df.groupby("mnth")["cnt"].sum()
    dataset_all = dataset_all.rename(index=month_names)
    return dataset_all


# Fungsi untuk menggabungkan data berdasarkan bulan
def combine_data_by_month(df):
    month_indices = df.groupby("mnth")["cnt"].sum().index
    month_names = [calendar.month_name[i] for i in month_indices]
    monthly_data = df.groupby("mnth")["cnt"].sum()
    monthly_data.index = month_names
    
    return monthly_data









# fungsi menggabungkan data berdasarkan tahun
def combine_yearly_total(df):
    yearly_total = df.groupby("yr")["cnt"].sum()
    yearly_total.index = yearly_total.index.map({0: "2011", 1: "2012"})
    return yearly_total


# Fungsi untuk menghitung total penyewaan berdasarkan workingday
def calculate_workingday_counts(df):
    workingday_counts = df.groupby("workingday")["cnt"].sum()
    workingday_counts.index = workingday_counts.index.map({0: "Holiday", 1: "Weekday"})
    return workingday_counts

def show_workingday(df):
    workingday_show = (df[df["workingday"] == 1]["cnt"]).sum()
    return workingday_show

def show_holiday(df):
    holiday_show = (df[df["workingday"] == 0]["cnt"]).sum()
    return holiday_show


main_df = pd.read_csv("dashboard/main_data.csv")

datetime_columns = ["dteday"]


main_df.sort_values(by="dteday", inplace=True)


main_df.reset_index(inplace=True, drop=True)


for column in datetime_columns:
    main_df[column] = pd.to_datetime(main_df["dteday"])

min_date = main_df["dteday"].min()
max_date = main_df["dteday"].max()

with st.sidebar:
    st.image("dashboard/logo.png")

    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )
    real_df = main_df[
        (main_df["dteday"] >= str(start_date)) & (main_df["dteday"] <= str(end_date))
    ]

all_rental = create_data_all(real_df)
data_by_month = combine_data_by_month(real_df)
data_by_year = combine_yearly_total(real_df)
count_working_day = calculate_workingday_counts(real_df)
holiday = show_holiday(real_df)
weekday = show_workingday(real_df)

total_rentals = real_df["cnt"].sum()

card_style = """
    background-color: #f4f4f4;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 2px 2px 10px 0px #000000;
    width: 30%;  /* Adjust the width as needed */
    display: inline-block;
    margin: 10px;
    """

# Create a layout with three side-by-side cards
st.header("Bicycle rental")

cards_html = f"""
<div style="display: flex; justify-content: space-between;">
    <div style="{card_style}">
        <h3>Total</h3>
        <p style="color: #009688; font-weight: bold; font-size: 24px;">{total_rentals}</p>
    </div>
    <div style="{card_style}">
        <h3>Working days</h3>
        <p style="color: #009688; font-weight: bold; font-size: 24px;">{weekday}</p>
    </div>
    <div style="{card_style}">
        <h3>Holidays</h3>
        <p style="color: #009688; font-weight: bold; font-size: 24px;">{holiday}</p>
    </div>
</div>
"""

st.markdown(cards_html, unsafe_allow_html=True)

st.subheader("Total Bicycle Rentals all time")
st.line_chart(all_rental)

st.subheader("Total Bicycle Rentals month")
st.bar_chart(data_by_month)

st.subheader("Total Bicycle Rentals year")
st.bar_chart(data_by_year)

st.header("Bicycle rental ")
st.subheader("Total Bicycle Rentals year")

fig, ax = plt.subplots()
ax.pie(count_working_day, labels=count_working_day.index, autopct="%1.1f%%", startangle=90)
ax.axis("equal")

st.pyplot(fig)
