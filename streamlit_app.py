# Import python packages
import streamlit as st
import requests
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(":cup_with_straw: Customize With Smoothie :cup_with_straw:")
st.write(
  """Choose The Fruits In Your Custom Smoothie
  """
)

name_on_order = st.text_input("Name On Order")
st.write("The name on the order is", name_on_order)

# option = st.selectbox(
#     "What Is Your Favorite Fruit?",
#     ("Banana", "Strawberries", "Peaches"),
# )

# st.write("You selected:", option)

# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
    # st.write(ingredients_list);
    # st.text(ingredients_list);
    ingredients_string = ''
    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      
        st.subheader(each_fruit + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + each_fruit)
        # st.text(smoothiefroot_response.json())
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # st.text(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+ name_on_order+ """')"""

    # st.write(my_insert_stmt)
    # st.stop()

    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")












    
