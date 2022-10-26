import streamlit
import pandas as pd
import snowflake.connector
import requests
from urllib.error import URLError

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
streamlit.header('Fruityvice Fruit Advice!')
fruityvice_repsonse = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
fruityvice_normalized = pd.json_normalize(fruityvice_repsonse.json())

streamlit.dataframe(fruityvice_normalized)

#não rode anythingpast here, OKIE?
#streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
add_my_fruit = streamlit.text_input('Digite o nome da fruta que você quer')
streamlit.write('Thanks for adding ', add_my_fruit)
my_cur.execute("insert into fruit_load_list values ('from steamlit')")
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)


