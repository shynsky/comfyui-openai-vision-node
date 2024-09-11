import torch
import base64
import requests
from io import BytesIO
from PIL import Image
import numpy as np

class OpenAIVisionNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "prompt": ("STRING", {"multiline": True}),
                "api_key": ("STRING", {"default": ""}),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "analyze_image"
    CATEGORY = "image/analysis"

    def analyze_image(self, image, prompt, api_key):
        try:
            # Debug: Print image shape
            print(f"Image shape: {image.shape}")
            
            # Convert the PyTorch tensor to a PIL Image
            image = image.squeeze().permute(1, 2, 0)
            image = (image * 255).clamp(0, 255).cpu().numpy().astype(np.uint8)
            pil_image = Image.fromarray(image)

            # Convert the image to base64
            buffered = BytesIO()
            pil_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            payload = {
                "model": "gpt-4-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img_str}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 300
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            
            if response.status_code == 200:
                return (response.json()['choices'][0]['message']['content'],)
            else:
                return (f"Error: {response.status_code}, {response.text}",)
        
        except Exception as e:
            # If an error occurs, return the error message
            return (f"Error in analyze_image: {str(e)}",)

NODE_CLASS_MAPPINGS = {
    "OpenAIVisionNode": OpenAIVisionNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OpenAIVisionNode": "OpenAI Vision Analysis"
}