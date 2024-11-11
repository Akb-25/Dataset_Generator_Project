import streamlit as st
from PIL import Image
from image_generator import generate_image
from prompt_generator import generate_prompts_with_titan
from image_modifier import generate_more_images
from datetime import datetime
import os
import base64

if "datasets" not in st.session_state:
    st.session_state["datasets"] = {}  
def update_dataset_in_memory(name, description, new_prompts, new_image_paths):
    if name in st.session_state["datasets"]:
        st.session_state["datasets"][name]["prompts"].extend(new_prompts)
        st.session_state["datasets"][name]["image_paths"].extend(new_image_paths)
        st.session_state["datasets"][name]["timestamp"] = datetime.now()  # Update timestamp
    else:
        st.error("Dataset is not there in memory")
def save_dataset_in_memory(name, description, prompts, image_paths):
    st.session_state["datasets"][name] = {
        "description": description,
        "prompts": prompts,
        "image_paths": image_paths,
        "timestamp": datetime.now()
    }

def get_image_paths(dataset_name):
    dataset = st.session_state["datasets"].get(dataset_name)
    if dataset:
        return dataset["image_paths"]
    return []

st.title("Artificial Image Dataset Generator")
st.write("Enter details to generate a new dataset.")

name = st.text_input("Dataset Name")
description = st.text_area("Dataset Description")
prompt = st.text_input("Additional Prompt")
height = st.number_input("Image Height", min_value=512, value=512)
width = st.number_input("Image Width", min_value=512, value=512)
number = st.number_input("Number of images you want to generate", min_value=1, value=1, max_value=100)

if st.button("Generate Dataset"):
    if name and description:
        try:
            prompts = generate_prompts_with_titan(name, description, prompt, number)

            for i,prompt in enumerate(prompts):
                st.write(f"{prompt}")

            image_paths = []  
            
            image_paths = generate_image(height, width, name, description, prompts)

            save_dataset_in_memory(name, description, prompts, image_paths)
            st.success("Dataset generated and saved in memory!")
        
        except Exception as e:
            st.error("Error generating dataset: " + str(e))
    else:
        st.warning("Please fill all required fields.")

if st.button("Show generated dataset"):
    st.write(st.session_state["datasets"])
    if name:
        image_paths = get_image_paths(name)
        if image_paths:
            for i in range(0, len(image_paths), 3):
                cols = st.columns(3)
                for j, path in enumerate(image_paths[i:i+3]):
                    img = Image.open(path) 
                    cols[j].image(img, caption=f"Generated Image {i+j+1}", use_container_width=True)
        else:
            st.warning("No images found for this dataset.")
    else:
        st.warning("Please enter a dataset name.")

st.header("Generate Similar Images")
image_number = st.text_input("Image Number")
number_images = st.number_input("Number of images to generate", min_value=1, value=1, max_value=5)

if st.button("Generate similar images"):
    if image_number:
        image_path = f"images/{name}_image_{image_number}.png"
        if os.path.exists(image_path): 
            image_paths = generate_more_images(name, description, prompt, image_path, height, width, number_images)
            update_dataset_in_memory(name, description, prompt, image_paths)
            st.success("Similar images generated and saved in memory!")
        else:
            st.warning("No images found for this dataset.")