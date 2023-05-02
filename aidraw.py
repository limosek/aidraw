#!/usr/bin/env python3

import argparse
import logging
import os
import sys
import requests
import json

# parse the command-line arguments
parser = argparse.ArgumentParser(description='Generate an image using the OpenAI API')
parser.add_argument('sentence', nargs="+", type=str, help='The prompt sentence for image generation')
parser.add_argument('--size', type=str, default='256x256', help='The size of the generated image')
parser.add_argument('--count', type=int, default=1, help='Number of images to generate')
parser.add_argument('--model', type=str, default='image-alpha-001', help='The ID of the model to use for image generation')
parser.add_argument('--key', type=str, help='The API key for the OpenAI API. You can use OPENAI_API_KEY env variable too')
parser.add_argument('--output', type=str, default='images/{sentence}/aidraw-{num}.jpg', required=False, help='Save image[s] to this directory')
args = parser.parse_args()

if not args.key:
    if os.getenv("OPENAI_API_KEY"):
        args.key = os.getenv("OPENAI_API_KEY")
    else:
        logging.getLogger().error("You need to set openai key! See aidraw.py -h")
        sys.exit()

# set up the API endpoint and headers
endpoint = 'https://api.openai.com/v1/images/generations'
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {args.key}'
}

# set up the request parameters
data = {
    'model': args.model,
    'prompt': " ".join(args.sentence),
    'num_images': args.count,
    'size': args.size,
    'response_format': 'url'
}

# send the request and parse the response
response = requests.post(endpoint, headers=headers, data=json.dumps(data))
response.raise_for_status()
response_data = response.json()

i = 1
for urls in response_data['data']:
    # extract the image URL from the response
    image_url = urls['url']
    # download the image and save it to a file
    image_response = requests.get(image_url)
    file = args.output.replace("{sentence}", " ".join(args.sentence)).replace("{num}", str(i))
    if file.find("/") >= 0:
        dir = os.path.dirname(file)
        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)
    with open(file, 'wb') as f:
        f.write(image_response.content)
    i += 1

