import streamlit as st
import pandas as pd
import plotly.express as px
from read_me import *
from theory import *
from general_plots_eda import *
from magnitude_regressors import *
from magnitude_prophet import *
from depth_data_cleaning import *
from depth_prophet import *
from depth_regressors import *
from magnitude_rnn_lstm import *
from depth_rnn_lstm import *
from model_comparison import *
from mag_prophet_error import *
from references import *

st.cache(persist=True)
st.set_page_config(layout="wide")


def load_data():
    eq = pd.read_csv("all_month.csv")
    eq["date"] = pd.to_datetime(eq["date"])
    # seperating 'place' column and only consider city by seperating the location by ', '
    newdf = eq['place'].str.split(', ', expand=True)
    eq['location'] = newdf[1]
    eq_df = eq[['date', 'time', 'latitude', 'longitude', 'location', 'mag', 'depth', 'type']]
    return eq, eq_df


eq, eq_df = load_data()

with st.container():
    st.subheader("***🌏 Quake Forecaster 🌏***")



st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
    unsafe_allow_html=True,
)

query_params = st.experimental_get_query_params()
tabs = ["Home", "Visualize", "Predict","Compare Algorithms", "Read Me", "References and Sources"]
if "tab" in query_params:
    active_tab = query_params["tab"][0]
else:
    active_tab = "Home"

if active_tab not in tabs:
    st.experimental_set_query_params(tab="Home")
    active_tab = "Home"

li_items = "".join(
    f"""
    <li class="nav-item">
        <a class="nav-link{' active' if t == active_tab else ''}" href="/?tab={t}">{t}</a>
    </li>
    """
    for t in tabs
)
tabs_html = f"""
    <ul class="nav nav-tabs">
    {li_items}
    </ul>
"""

st.markdown(tabs_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if active_tab == "Home":
    st.sidebar.title("**Quake Forecaster**")  # ** to bold the text
    quote()
    st.image("eq1.png")      #https://docs.streamlit.io/library/api-reference/media/st.image
    theory1()
    st.image("eq2_shaanxi.jpg", caption= " The deadliest Shaanxi(China) Earthquake, 1556. " )
    st.image("eq3_lomaprieta.jpg", caption=" The deadliest Loma Prieta(San Francisco) Earthquake, 1989. ")
    theory2()
    home_sidebar()


if active_tab == "Visualize":

    st.sidebar.title('**Earthquake Dashborad**')
    st.sidebar.markdown(''' 

    Select the different options to vary the Visualization.\n
    All the Charts are interactive.\n
    Scroll the mouse over the Charts to feel the interactive features like Tool tip, Zoom, Pan ''')

    st.header("General Analysis")
    view_data()
    gen_analysis()
    type = st.sidebar.radio("Select the type of Chart", ('Number of Events Occured',
                                                             'Percentage of Events per Month',
                                                             'Proportion of Events',
                                                             'Number of Earthquake Events',
                                                             'Magnitude Repartitions',
                                                             'Depth Repartitions',
                                                             'Places with Highest Magnitudes',
                                                             'Places with Highest Depths',
                                                             'Distribution of earthquakes w.r.t. to Magnitude',
                                                             'Distribution of earthquakes w.r.t. to Depth',
                                                             'Distribution of Magnitude over the period',
                                                             'Distribution of Depth over the period'
                                                             ))

    if type == 'Number of Events Occured':
        number_of_events_occured()

    elif type == 'Percentage of Events per Month':
        percentage_of_events_per_month()

    elif type == 'Proportion of Events':
        proportion_of_events()

    elif type == 'Number of Earthquake Events':
        number_of_earthquake_events()

    elif type == 'Magnitude Repartitions':
        magnitude_repartitions()

    elif type == 'Depth Repartitions':
        depth_repartitions()

    elif type == 'Places with Highest Magnitudes':
        places_with_highest_mags()

    elif type == 'Places with Highest Depths':
        places_with_highest_depths()

    elif type == 'Distribution of earthquakes w.r.t. to Magnitude':
        eq_distr_w_r_t_magnitude()

    elif type == 'Distribution of earthquakes w.r.t. to Depth':
        eq_distr_w_r_t_depth()

    elif type == 'Distribution of Magnitude over the period':
        eq_mag_scatter()

    elif type == 'Distribution of Depth over the period':
        eq_depth_scatter()

    st.sidebar.image("earth-unscreen.gif")

if active_tab == "Predict":
    st.sidebar.title('Earthquake Time Series Predictor')
    st.sidebar.markdown(''' 

        Select the different parameter and options to vary the prediction algorithms.\n 
        Click the "Predict" button once you have done selecting the prediction algorithm.\n
        Hover the mouse over the charts to feel the interactive features like Tool tip, Zoom, and Pan.

     ''')

    st.header("Time Series Prediction")
    parameter = st.sidebar.selectbox("Select the parameter", ('Magnitude', 'Depth'))
    training_model = st.sidebar.selectbox("Select the Training Model", ('Facebook Prophet', 'Regression', 'LSTM'))
    if parameter == 'Magnitude':
        st.write("Prediction with respect to Earthquake Magnitude")


        if training_model == 'Facebook Prophet':
            predict_prophet = st.sidebar.button("Predict")
            st.subheader("Facebook Prophet")
            prophet_info()
            if predict_prophet:
                gif_runner = st.image('earth-unscreen.gif')
                mag_prophet()
                gif_runner.empty()

        if training_model == 'Regression':
            predict_reg = st.sidebar.button("Predict")
            st.subheader("Regression")
            reg_info()
            if predict_reg:
                gif_runner = st.image('earth-unscreen.gif')
                mag_regressions()
                gif_runner.empty()

        if training_model == 'LSTM':
            predict_lstm = st.sidebar.button("Predict")
            st.subheader("Long Short-Term Memory Network")
            lstm_info()
            if predict_lstm:
                gif_runner = st.image('earth-unscreen.gif')
                mag_lstm()
                gif_runner.empty()



    if parameter == "Depth":
        st.write("Prediction with respect to Earthquake Depth")


        if training_model == 'Facebook Prophet':
            predict_prophet = st.sidebar.button("Predict")
            st.subheader("Facebook Prophet")
            prophet_info()
            if predict_prophet:
                gif_runner = st.image('earth-unscreen.gif')
                dep_prophet()
                gif_runner.empty()

        if training_model == 'Regression':
            predict_reg = st.sidebar.button("Predict")
            st.subheader("Regression")
            reg_info()
            if predict_reg:
                gif_runner = st.image('earth-unscreen.gif')
                dep_regressions()
                gif_runner.empty()

        if training_model == 'LSTM':
            predict_lstm = st.sidebar.button("Predict")
            st.subheader("Long Short-Term Memory Network")
            lstm_info()
            if predict_lstm:
                gif_runner = st.image('earth-unscreen.gif')
                dep_lstm()
                gif_runner.empty()




if active_tab == "Compare Algorithms":
    compare_info()
    st.sidebar.markdown(''' 

            Select the different parameter and options to vary the parameters.\n 
            Click the "Compare" button once you have done selecting the parameter.\n
            Hover the mouse over the charts to feel the interactive features like Tool tip, Zoom, and Pan.

         ''')
    st.sidebar.title('Algorithm Comparison')
    cmp_parameter = st.sidebar.radio("Select the parameter", ('Magnitude', 'Depth'))
    if cmp_parameter == 'Magnitude':
        cmp_mag = st.sidebar.button("Compare")
        if cmp_mag:
            gif_runner = st.image('earth-unscreen.gif')
            st.write("Listed below are the various algorithms used in this work along with their respective Mean Squared Errors.")
            compare_mag_models()

            gif_runner.empty()


    if cmp_parameter == 'Depth':
        cmp_dep = st.sidebar.button("Compare")
        if cmp_dep:
            gif_runner = st.image('earth-unscreen.gif')
            st.write("Listed below are the various algorithms used in this work along with their respective Mean Squared Errors.")
            compare_dep_models()
            gif_runner.empty()




if active_tab == "Read Me":
    readme_1()



if active_tab == "References and Sources":
    sources()
    ref()
    other_links()


