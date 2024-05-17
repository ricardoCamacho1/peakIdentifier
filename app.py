import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.signal import find_peaks, peak_prominences, peak_widths

# Streamlit app title
st.title('Peak Identifiers')
st.write('This is a simple web app that identifies peaks in a given dataset and compares the first peak to subsequent ones.')

# File uploader
st.sidebar.subheader('Here you can upload your dataset to identify peaks and compare them:')
uploaded_file = st.sidebar.file_uploader("Choose a file")

def get_peaks(data):
    # Calculating mean and standard deviation
    mean_voltage = data['Wl-ShootingVoltage'].mean()
    std_voltage = data['Wl-ShootingVoltage'].std()

    # Threshold for significant negative peaks
    std_threshold = mean_voltage - 3 * std_voltage

    # Inverting the voltage to identify negative peaks as positive
    inverted_voltage = -data['Wl-ShootingVoltage']

    # Finding peaks with the calculated threshold
    negative_peaks, _ = find_peaks(inverted_voltage, height=abs(std_threshold))

    # Calculating peak properties
    prominences = peak_prominences(inverted_voltage, negative_peaks)[0]
    widths = peak_widths(inverted_voltage, negative_peaks, rel_height=0.5)[0]

    # Creating a DataFrame for peak details
    peak_details = pd.DataFrame({
        'Time': data['Time'][negative_peaks],
        'Voltage': data['Wl-ShootingVoltage'][negative_peaks],
        'Depth': data['Wl-Depth'][negative_peaks],
        'Prominence': prominences,
        'Width': widths
    })

    return peak_details, negative_peaks, std_threshold

def plot_peaks(data, negative_peaks, std_threshold):
    # Plotting the data and peaks
    fig = px.line(data, x='Time', y='Wl-ShootingVoltage', title='Negative Peaks in Shooting Voltage')
    fig.add_scatter(x=data['Time'][negative_peaks], y=data['Wl-ShootingVoltage'][negative_peaks], mode='markers', name='Peaks', marker=dict(color='red'))
    fig.add_hline(y=std_threshold, line_dash='dash', line_color='red', annotation_text='Threshold: {:.2f}'.format(std_threshold), annotation_position='bottom right')
    return fig

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['Time'] = pd.to_datetime(df['Time'])
    st.header('Data Overview:')
    st.write(df)
    fig = px.line(df, x='Time', y='Wl-ShootingVoltage', title='Shooting Voltage Over Time')
    st.plotly_chart(fig)

    peak_details, negative_peaks, std_threshold = get_peaks(df)

    st.header('Peak Details:')
    st.dataframe(peak_details)

    # Comparing the first peak with the others
    if len(peak_details) > 1:
        first_peak = peak_details.iloc[0]
        average_prominence = peak_details['Prominence'][1:].mean()
        average_width = peak_details['Width'][1:].mean()
        st.subheader('Comparison with First Peak:')
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Prominence Difference", value="{:.2f}".format(first_peak['Prominence'] - average_prominence))
        with col2:
            st.metric(label="Width Difference", value="{:.2f}".format(first_peak['Width'] - average_width))

    st.subheader('Peak Visualization:')
    fig = plot_peaks(df, negative_peaks, std_threshold)
    st.plotly_chart(fig)
