# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd
session = st.connection('snowflake').session()

# Write directly to the app
st.title(f":cup_with_straw: \
Customize your smoothie! \
:cup_with_straw: ")

name_on_order = st.text_input('Name on Smoothie:')


my_dataframe = session.table("smoothies.public.fruit_options")\
                .select(col('FRUIT_NAME'), col('SEARCH_ON'))

#st.dataframe(my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()





ingredients_list = st.multiselect(
    'Choose up to 5 ingridients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get(f'https://my.smoothiefroot.com/api/fruit/{search_on}')
        sf_df = st.dataframe(smoothiefroot_response.json(), use_container_width=True)


    # This is a SQL statement
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """',\
            '"""+ name_on_order + """')"""


    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your smoothie is ordered', icon="✅")

     
