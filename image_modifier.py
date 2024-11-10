# import base64
# import boto3
# import json
# import os
# import random
# import sqlite3
# from datetime import datetime


# client = boto3.client("bedrock-runtime", region_name="us-east-1")
# model_id = "amazon.titan-image-generator-v1"

# output_dir = "images"
# def generate_more_images(name, description, prompt, base_image_path, height, width, num_images=5):
#     conn = sqlite3.connect('datasets.db')
#     cursor = conn.cursor()
#     with open(base_image_path, "rb") as image_file:
#         base_image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

#     native_request = {
#         "imageVariationParams": {
#             "text": "generate more images that look like this",
#             "images": [base_image_base64]  # Include the base image for variation
#         },
#         "taskType": "IMAGE_VARIATION",
#         "imageGenerationConfig": {
#             "cfgScale": 8,
#             "seed": 0,
#             "width": width,
#             "height": height,
#             "numberOfImages": num_images
#         }
#     }

#     request = json.dumps(native_request)
#     response = client.invoke_model(modelId=model_id, body=request)
#     model_response = json.loads(response["body"].read())

#     for i in range(len(model_response["images"])):
#         base64_image_data = model_response["images"][i]
#         image_data = base64.b64decode(base64_image_data)
#         image_path = os.path.join(output_dir, f"titan_new_{i}.png")
#         with open(image_path, "wb") as file:
#             file.write(image_data)  
#         print(f"The generated image has been saved to {image_path}.")
        
#         cursor.execute("INSERT INTO datasets (name, description, prompt, image_url, timestamp) VALUES (?, ?, ?, ?, ?)",
#                            (name, description, prompt, image_path, datetime.now()))
#         conn.commit()
#     conn.close()

import base64
import boto3
import json
import os
import random
from datetime import datetime

client = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = "amazon.titan-image-generator-v1"

output_dir = "images"
os.makedirs(output_dir, exist_ok=True)

datasets_in_memory = {}

def generate_more_images(name, description, prompt, base_image_path, height, width, num_images=5):
    with open(base_image_path, "rb") as image_file:
        base_image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    native_request = {
        "imageVariationParams": {
            "text": "generate more images that look like this image but have very slight differences ",
            "images": [base_image_base64]  
        },
        "taskType": "IMAGE_VARIATION",
        "imageGenerationConfig": {
            "cfgScale": 8,
            "seed": random.randint(0, 2147483647),
            "width": width,
            "height": height,
            "numberOfImages": num_images
        }
    }
    request = json.dumps(native_request)
    response = client.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())

    image_paths = []

    for i, base64_image_data in enumerate(model_response["images"]):
        num_random = random.randint(0, 2147483647)
        image_data = base64.b64decode(base64_image_data)
        image_path = os.path.join(output_dir, f"{name}_variation_{i}_{num_random}.png")
        
        with open(image_path, "wb") as file:
            file.write(image_data)
        
        print(f"The generated image has been saved to {image_path}.")
        image_paths.append(image_path)  

    # datasets_in_memory[name] = {
    #     "description": description,
    #     "prompt": prompt,
    #     "base_image": base_image_path,
    #     "generated_images": image_paths,
    #     "timestamp": datetime.now()
    # }

    print(f"Dataset '{name}' generated and stored in memory.")
   
    return image_paths

if __name__ == "__main__":
    base_image_path = "images/sample_base_image.png"  # Example image path
    generate_more_images(
        name="SampleDataset",
        description="Sample description for generating similar images",
        prompt="Generate variations of this image",
        base_image_path=base_image_path,
        height=512,
        width=512,
        num_images=5
    )

    print("In-memory datasets:")
    print(datasets_in_memory)