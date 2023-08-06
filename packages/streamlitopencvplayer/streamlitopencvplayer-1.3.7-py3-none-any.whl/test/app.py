import streamlit as st

num_buttons = 5

for i in range(num_buttons):
    button_label = f'Button {i+1}'
    button_clicked = st.button(button_label)
    if button_clicked:
        st.write(f'Button "{button_label}" was clicked!')
