import streamlit
import pandas as pd

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu!')
streamlit.text('🥣 Omega 3 & Blueberry Oatamal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit2 = my_fruit.set_index('Fruit')
#######################################
fruits_select= streamlit.multiselect("Pick some fruits:", list(my_fruit2.index),["Apple", "Banana"])
fruits_show = my_fruit2.loc[fruits_select]
                      
streamlit.dataframe(fruits_show)

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

#New scena
import requests
streamlit.header('Fruityvice Fruit Advice!')
fruityvice_repsonse = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
fruityvice_normalized = pd.json_normalize(fruityvice_repsonse.json())

streamlit.dataframe(fruityvice_normalized)


import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("The fruit load list contains:")
streamlit.text(my_data_row)
