import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Title of app
st.title("My Parents New Healthy Diner")
st.write('Breakfast Menu\n' + 
         'Omega 3 & Blueberry Oatmeal\n' + 
         'Kale, Spinach & Rocket Smoothie\n' + 
         'Hard-Boiled Free-Range Egg')

# Name on the order
name_on_order = st.text_input("Name on Smoothie")
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cns.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections = 5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
