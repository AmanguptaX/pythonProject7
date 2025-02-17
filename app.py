import streamlit as st
import pandas as pd
import datetime

def assign_nutritionists(clients_df, nutritionists):
    start_time = datetime.datetime.strptime("09:00", "%H:%M")
    end_time = datetime.datetime.strptime("18:00", "%H:%M")
    lunch_start = datetime.datetime.strptime("13:00", "%H:%M")
    lunch_end = datetime.datetime.strptime("14:00", "%H:%M")
    consult_duration = datetime.timedelta(minutes=30)

    schedule = []
    nutritionist_times = {n: start_time for n in nutritionists}

    for i, row in clients_df.iterrows():
        current_nutritionist = min(nutritionist_times, key=nutritionist_times.get)
        assigned_time = nutritionist_times[current_nutritionist]

        if lunch_start <= assigned_time < lunch_end:
            assigned_time = lunch_end

        if assigned_time >= end_time:
            st.error("Consultations exceed working hours. Reduce client count or increase nutritionists.")
            return pd.DataFrame()

        schedule.append({
            "S No": row["S No"],
            "Client Name": row["Name"],
            "Nutritionist": current_nutritionist,
            "Consultation Time": assigned_time.strftime("%H:%M")
        })

        nutritionist_times[current_nutritionist] += consult_duration

    return pd.DataFrame(schedule)

st.title("Auto Assign Nutritionists to Clients")

uploaded_file = st.file_uploader("Upload Client Excel File", type=["xlsx", "xls"])

if uploaded_file:
    clients_df = pd.read_excel(uploaded_file)

    st.write("Preview of Uploaded Data:", clients_df.head())

    num_nutritionists = st.number_input("Enter Number of Available Nutritionists", min_value=1, step=1)

    nutritionists = []
    for i in range(num_nutritionists):
        nutritionist_name = st.text_input(f"Enter Name of Nutritionist {i + 1}")
        if nutritionist_name:
            nutritionists.append(nutritionist_name)

    if st.button("Assign Nutritionists") and len(nutritionists) == num_nutritionists:
        result_df = assign_nutritionists(clients_df, nutritionists)

        if not result_df.empty:
            st.write("### Assignment Result")
            st.dataframe(result_df)

            output_file = "nutritionist_assignment.xlsx"
            result_df.to_excel(output_file, index=False)

            with open(output_file, "rb") as f:
                st.download_button("Download Result", f, file_name=output_file)
