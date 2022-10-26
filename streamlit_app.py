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

streamlit.header('🥝🍇🍌🥭 Build Your Own Fruit Smoothie 🥝🍇🍌🥭')

#Lendo o csv
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list2 = my_fruit_list.set_index('Fruit')

# Vamos colocar uma lista de escolha aqui para que eles possam escolher as frutas que desejam incluir
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list2.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list2.loc[fruits_selected]

# Display da Pagina
streamlit.dataframe(fruits_to_show)
#### HEADER #####
streamlit.header("Fruityvice Fruit Advice!")

#Função e validação

def get_fruityvice_data(this_fruit_choice):
  streamlit.write('The user entered ', this_fruit_choice)
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  #####
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
                                     
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information")
  else:

    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
  
except:
  streamlit.error()
  


streamlit.header("The fruit_load_list contains:")
#Snowflake related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()
  
#adciona um botão
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

#Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute(f"insert into fruit_load_list values ('{new_fruit}')")
    return "Thanks for adding " + new_fruit

 #Variavel pra adionar mais frutas.
add_my_fruit = streamlit.text_input('What fruit would you like information about?','jackfruit')
#IF pra validar o que tem dentro do snow
if streamlit.button('Add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(back_from_function)
