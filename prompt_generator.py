import boto3
from botocore.exceptions import ClientError

client = boto3.client("bedrock-runtime", region_name="ap-south-1")
model_id = "amazon.titan-text-express-v1"

def generate_prompts_with_titan(dataset_name, description, additional_prompt, number):
    titan_prompt = (
        f"Generate {number} unique, detailed, descriptive prompts for creating images in the following dataset.\n\n"
        f"- **Dataset Name**: {dataset_name}\n"
        f"- **Dataset Description**: {description}\n"
        f"- **Additional Instructions**: {additional_prompt}\n\n"
        f"Each prompt should provide specific visual details, context, and style relevant to this dataset, "
        f"helping to generate a variety of high-quality images. List each prompt on a new line or in a numbered list."
    )

    conversation = [
        {
            "role": "user", 
            "content": [{"text": titan_prompt}]
        }
    ]

    try:
        response = client.converse(
            modelId="amazon.titan-text-express-v1",
            messages=conversation,
            inferenceConfig={
                "maxTokens": 2048,
                "stopSequences": ["User:"],
                "temperature": 0,
                "topP": 1
            },
            additionalModelRequestFields={}
        )

        response_text = response["output"]["message"]["content"][0]["text"]

        prompts = [line.strip() for line in response_text.splitlines() if line.strip()]

        if len(prompts) > 100:
            prompts = prompts[:100]
        
        return prompts[1:]

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke 'amazon.titan-text-express-v1'. Reason: {e}")
        exit(1)

if __name__ == "__main__":

    dataset_name = "Urban Wildlife Photography"
    description = "Images of animals interacting with city environments, capturing the contrast between urban structures and wildlife."
    additional_prompt = "Focus on lighting that highlights the urban-wildlife contrast, capturing both daytime and nighttime scenes."

    prompts = generate_prompts_with_titan(dataset_name, description, additional_prompt, number)

    print("Generated Prompts :", prompts)
    print("Total Prompts Generated:", len(prompts))  