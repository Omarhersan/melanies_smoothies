# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
session = get_active_session()


# Write directly to the app
st.title(f":cup_with_straw: \
Customize your smoothie! \
:cup_with_straw: ")

name_on_order = st.text_input('Name on Smoothie:')


my_dataframe = session.table("smoothies.public.fruit_options")\
                .select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingridients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # This is a SQL statement
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """',\
            '"""+ name_on_order + """')"""


    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your smoothie is ordered', icon="✅")

        

