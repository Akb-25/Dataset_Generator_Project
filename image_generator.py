# import base64
# import boto3
# import json
# import os
# import random
# import sqlite3
# from datetime import datetime


# client = boto3.client("bedrock-runtime")
# model_id = "amazon.titan-image-generator-v1"

# seed = random.randint(0, 2147483647)

# def generate_image(height, width, name, description, prompts=None):
#     conn = sqlite3.connect('datasets.db')
#     cursor = conn.cursor()
#     i = 0
#     for prompt in prompts:
#         native_request = {
#             "taskType": "TEXT_IMAGE",
#             "textToImageParams": {"text": prompt},
#             "imageGenerationConfig": {
#                 "numberOfImages": 1,
#                 "quality": "standard",
#                 "cfgScale": 8.0,
#                 "height": height,
#                 "width": width,
#                 "seed": seed,
#             },
#         }

#         request = json.dumps(native_request)
#         response = client.invoke_model(modelId=model_id, body=request)
#         model_response = json.loads(response["body"].read())

#         base64_image_data = model_response["images"][0]
#         image_data = base64.b64decode(base64_image_data)
#         output_dir = "images"
#         image_path = os.path.join(output_dir, f"titan_{i}.png")
        
#         with open(image_path, "wb") as file:
#             file.write(image_data)

#         cursor.execute("INSERT INTO datasets (name, description, prompt, image_url, timestamp) VALUES (?, ?, ?, ?, ?)",
#                            (name, description, prompt, image_path, datetime.now()))
#         conn.commit()
#         print(f"The generated image has been saved to {image_path}")
#         i += 1
#     conn.close()


# if __name__ == "__main__":
#     prompts = [
#         "A photo of a cat",
#         "A photo of a dog",
#         "A photo of a cat",
#         "A photo of a dog",
#         "A photo of a cat",
#         "A photo of a dog",
#         "A photo of a cat",
#         "A photo of a dog",
#         "A photo of a cat",
#         "A photo of a dog",
#     ]

#     generate_image(prompts)

import base64
import boto3
import json
import os
import random
from datetime import datetime

client = boto3.client("bedrock-runtime", region_name="ap-south-1")
model_id = "amazon.titan-image-generator-v1"

seed = random.randint(0, 2147483647)

datasets_in_memory = {}

def generate_image(height, width, name, description, prompts=None):
    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)

    image_paths = []

    for i, prompt in enumerate(prompts):
        native_request = {
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {"text": prompt},
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "quality": "standard",
                "cfgScale": 8.0,
                "height": height,
                "width": width,
                "seed": seed,
            },
        }

        request = json.dumps(native_request)
        response = client.invoke_model(modelId=model_id, body=request)
        model_response = json.loads(response["body"].read())

        base64_image_data = model_response["images"][0]
        image_data = base64.b64decode(base64_image_data)
        image_path = os.path.join(output_dir, f"{name}_image_{i}.png")
        
        with open(image_path, "wb") as file:
            file.write(image_data)

        image_paths.append(image_path)
        print(f"The generated image has been saved to {image_path}")

    datasets_in_memory[name] = {
        "description": description,
        "prompts": prompts,
        "image_paths": image_paths,
        "timestamp": datetime.now()
    }
    return image_paths

if __name__ == "__main__":
    prompts = [
        "A photo of a cat",
        "A photo of a dog",
        "A photo of a sunset over mountains",
        "A photo of a beach with palm trees",
        "A photo of a snowy forest",
    ]

    generate_image(height=512, width=512, name="SampleDataset", description="Sample description", prompts=prompts)

    print("Generated dataset stored in memory:")
    print(datasets_in_memory)