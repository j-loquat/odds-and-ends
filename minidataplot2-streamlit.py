# minidataplot2-streamlit.py

import streamlit as st
import pandas as pd
import plotly.express as px

# ---- Creating global Dictionary of sample fuits data to model with ----
_dic = {
    'Fruit Type': ['Blueberry', 'Avacado', 'Banana'],
    'Quantity': [45, 28, 30]
}

def init_page():
    # Initialize page session state
    if "dataloaded" not in st.session_state:
        st.session_state.dataloaded = False

    # setup page and columns
    st.set_page_config(
        page_title="Streamlit Fruit Data Plot",
        page_icon=":bar_chart:",
        layout="wide"
    )
    data_column, plot_column = st.columns((1,2))

    # setup initial display text
    data_column.header('Fruits List')
    data_column.write('This is a test page for making simple plots.')
    data_column.write('Press the button to load the data dictionary.')

    # setup button
    load = data_column.button('Load Data')
    data_column.markdown('#')
    
    return load, data_column, plot_column

def main():
    load, data_column, plot_column = init_page()

    # if load button pressed now OR was pressed before, then this runs and plot choice shown
    # changing plotopt by clicking re-runs page, so need to run this again with load button
    if load or st.session_state.dataloaded:
        _df = pd.DataFrame(_dic)
        # data_column.write(_df) -> doing this shows pandas df with Index as first col
        data_column.dataframe(_df, hide_index=True, use_container_width=False)
        data_column.markdown('#')
        st.session_state.dataloaded = True

        plot_column.markdown('#')
        
        # ---- Plot types -------
        plotopt = plot_column.radio('Plot type :', ['Bar', 'Pie'])
        if plotopt == 'Bar':
            fig = px.bar(
                _df, x= 'Fruit Type',
                y = 'Quantity',
                title ='Fruit Bar Chart'
            )
            plot_column.plotly_chart(fig)
        
        else:     
            fig = px.pie(
                _df, names = 'Fruit Type',
                values = 'Quantity',
                title ='Fruit Pie Chart'
            )
            plot_column.plotly_chart(fig)
    
    st.write("---")  # divider

    # button to Reset
    if data_column.button(label="Reset", use_container_width=True):
        # re-run by simple reset of all session state info
        # delete all the items in Session state
        for key in st.session_state.keys():
            del st.session_state[key]
        # needed to re-trigger running from the top, otherwise waits on another press
        st.experimental_rerun()

if __name__ == "__main__":
    main()