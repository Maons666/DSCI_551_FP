import streamlit as st
import streamlit.components.v1 as components
import Submit_Interface
import Search_Interface

st.title("Lost and Found Center")
st.subheader("Do you want to submit lost & found information or search for recorded lost & found information?")

if 'page' not in st.session_state:
    st.session_state.page = None  # Initialize page state

col1, col2 = st.columns(2)

with col1:
    if st.button("Submit L & F info..."):
        st.session_state.page = 'submit'

with col2:
    if st.button("Search for L & F info..."):
        st.session_state.page = 'search'

if st.session_state.page == 'submit':
    Submit_Interface.SubmitPage()
elif st.session_state.page == 'search':
    Search_Interface.SearchPage()

    
# pip/conda install streamlit
    
# Change to the working directory and type the following line:
# streamlit run [filename]