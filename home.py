import streamlit as st
from page_init import page_init
from meeting_form import insert_meeting_form
# Microsoft Azure App Registration info:

# Application (client) ID:
# 837eeb79-b660-4038-a54c-a1117ed13f37

# Object ID:
# a051d8e3-63af-4a01-8c73-2d80533a95d4

# Directory (tenant) ID:
# f76c6a59-2c29-4223-ba16-573148719ce5

def main():

    c1, c2 = page_init()

    with st.container():
        with c1:  
            st.markdown("# Hi, I'm Kyan Nelson")
            st.markdown("##### *BS  Dual Emphasis in Finance and Information Management with Computer Science Integration*")
            st.markdown('''
                        - Phone Number:303-802-9736
                        - Email: kyan.nelson@colorado.edu
                        - LinkedIn: https://www.linkedin.com/in/kyan-nelson/                        
                        ''')

        with c2:
            st.image("static/headshot.png", width=400)

    st.header("Schedule a Coffee Chat:")
    insert_meeting_form()

if __name__ == "__main__":
    main()