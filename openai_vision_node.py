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
        # Debug: Print image type and shape
        print(f"Image type: {type(image)}")
        if isinstance(image, (torch.Tensor, np.ndarray)):
            print(f"Image shape: {image.shape}")

        # Convert the input to a PIL Image
        if isinstance(image, torch.Tensor):
            # If it's a PyTorch tensor
            if image.ndim == 4:
                image = image.squeeze(0)  # Remove batch dimension if present
            if image.shape[0] in [1, 3, 4]:  # If color channel is first
                image = image.permute(1, 2, 0)
            
            image = image.float().cpu().numpy()
            
            if image.max() <= 1.0:
                image = (image * 255).astype(np.uint8)
            else:
                image = image.astype(np.uint8)
            
            if image.shape[2] == 1:  # If it's grayscale
                image = np.squeeze(image, axis=2)
            elif image.shape[2] == 4:  # If it has an alpha channel
                image = image[:, :, :3]  # Remove alpha channel
        
        elif isinstance(image, np.ndarray):
            # If it's already a numpy array
            if image.ndim == 4:
                image = image.squeeze(0)  # Remove batch dimension if present
            if image.shape[0] in [1, 3, 4]:  # If color channel is first
                image = np.transpose(image, (1, 2, 0))
            
            if image.max() <= 1.0:
                image = (image * 255).astype(np.uint8)
            else:
                image = image.astype(np.uint8)
            
            if image.shape[2] == 1:  # If it's grayscale
                image = np.squeeze(image, axis=2)
            elif image.shape[2] == 4:  # If it has an alpha channel
                image = image[:, :, :3]  # Remove alpha channel

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

NODE_CLASS_MAPPINGS = {
    "OpenAIVisionNode": OpenAIVisionNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OpenAIVisionNode": "OpenAI Vision Analysis"
}
