###############################
# This program lets you       #
# - Create a dashboard        #
# - Every dashboard page is  #
# created in a separate file  #  
###############################

# Python libraries
import streamlit as st

# User module files:

from mr import *
import functions

def main():

  st.set_page_config(layout="wide")

#Containers:

  c1 = st.container()
  c2 = st.container()
  c3 = st.container()
  c4 = st.container()

#Song covers:

  cover1 = functions.get_cover('Stone Temple Pilots')
  cover2 = functions.get_cover('Chris Cornell')
  cover3 = functions.get_cover('Deep Purple')
  cover4 = functions.get_cover('Creedence Clearwater Revival')
  
    #############  
    # Main page #
    #############   

  
  with c1: 
    col1, col2, col3 = st.columns(3)

    with col2:
      st.image('images/logo.png')
      st.write("## Your music recommender")

    mr()
                 
  with c2:
      
      st.write('\n\n')
      st.write('\n\n')
      st.write('\n\n')

  with c3:
    col1, col2, col3 = st.columns([2,1,2])

    with col2: 
      st.write('#### Featured Recommendations:')

      st.write('\n\n')
      st.write('\n\n')
      st.write('\n\n')

  with c4: 
    col1, col2, col3, col4 = st.columns(4)

    with col1:

      st.image(cover1)

    with col2:
      st.image(cover2)

    with col3:
      st.image(cover3)

    with col4: 
      st.image(cover4)

    
main()
