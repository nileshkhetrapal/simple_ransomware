import requests
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
import os, time
import json

# Replace with valid values
ENDPOINT = "https://adamransomwaredetection.cognitiveservices.azure.com/"
prediction_key = "d0308db932914e2eb5d37410976a019b"
prediction_resource_id = "https://adamransomwaredetection-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/4d3b1920-50ab-4839-bac9-be1f1d68b5e3/classify/iterations/Iteration1/image"
# Function to perform spectrogram conversion
def def_spectrogram(filepath, directory):
    start_time = time.time()
    #if directory doesnt exist, create it
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Open the binary file and read its content into a bytearray
    with open(filepath, "rb") as f:
        #read the file
        binary_content = bytearray(f.read())
    # Convert the binary content into a time-domain signal
    signal = np.array(binary_content, dtype=float)
    
    # Check if the process has taken longer than 30 seconds
    elapsed_time = time.time() - start_time
    if elapsed_time > 30:
        print(f"Skipping file {filepath} as the process took longer than 30 seconds")
        return
    # Create the spectrogram visualization
    plt.specgram(signal, NFFT=1024, Fs=44100)
    # Place the labels
    # Place the title with the filename
    filename = os.path.basename(filepath)
    #put the gradient legend
    #Convert the plot to an image
    #Create the savefile path
    savefile = os.path.join(directory, filename + ".png")
    plt.savefig(savefile)
    # Save the plot as a png file
    plt.close()
    return savefile

# Function to send the spectrogram to the API and receive the prediction
def predict(filepath):
    # Add code to send the spectrogram to the API
    print("Sending request to API...")
    print("Filepath: " + filepath)
    # Replace the URL below with the actual API URL
    url = "https://adamransomwaredetection-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/4d3b1920-50ab-4839-bac9-be1f1d68b5e3/classify/iterations/Iteration1/image"
    headers = {
        "Prediction-Key": "d0308db932914e2eb5d37410976a019b",
        "Content-Type": "application/octet-stream"
    }
    image = open(filepath, "rb").read()
    # Send the request and get the response
    response = requests.post(url, headers=headers, data=image)
    # Convert the response to JSON
    response = json.loads(response.text)
    #This is the format of the response:
    # {'id': '03902057-4c85-460f-a608-faecfe4b5088', 'project': '4d3b1920-50ab-4839-bac9-be1f1d68b5e3', 'iteration': '5a1d2c42-6a82-44c5-83db-fee47a5eb786', 'created': '2023-02-13T00:10:48.984Z', 'predictions': [{'probability': 0.99554056, 'tagId': '9b97db47-c6b1-4702-a4f9-f173fec8600e', 'tagName': 'Benign'}, {'probability': 0.004459459, 'tagId': '1bc35583-aa73-44b7-a173-5bb4370bb273', 'tagName': 'Malign'}]}
    # Get the prediction with the highest probability
    prediction = max(response["predictions"], key=lambda x: x["probability"])
    probability = prediction["probability"]
    
    #print(f"Prediction: {prediction['tagName']}, Probability: {probability}")
    return prediction["tagName"], probability


def main():
    filepath = input("Enter the path to the file: ")
    #filepath = "/workspaces/simple_ransomware/ransomeware.py"
    if filepath:
        spectrogram_filepath = def_spectrogram(filepath, "spectrograms")
        result = predict(spectrogram_filepath)
        prediction , probability = result
        print("Prediction", f"Prediction: {prediction}, Probability: {probability}")
        #Remove the spectrogram
        os.remove(spectrogram_filepath)
        #Remove the spectrogram directory
        os.rmdir("spectrograms")

main()
