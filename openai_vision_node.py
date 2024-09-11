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
                "api_key": ("STRING", {"default": ""}),
            },
            "optional": {
                "custom_prompt": ("STRING", {"multiline": True, "default": "Describe the main fashion garment in this image, including its style, color, and notable features."}),
                "max_tokens": ("INT", {"default": 300, "min": 50, "max": 1000}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "analyze_fashion"
    CATEGORY = "image/fashion_analysis"

    def analyze_fashion(self, image, api_key, custom_prompt=None, max_tokens=300):
        try:
            if not api_key:
                raise ValueError("API key is required")

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

            prompt = custom_prompt or "Describe the main fashion garment in this image, including its style, color, and notable features."

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
                "max_tokens": max_tokens
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            
            if response.status_code == 200:
                return (response.json()['choices'][0]['message']['content'],)
            else:
                return (f"Error: {response.status_code}, {response.text}",)
        
        except ValueError as ve:
            return (f"Error: {str(ve)}",)
        except Exception as e:
            return (f"Error in analyze_fashion: {str(e)}",)

NODE_CLASS_MAPPINGS = {
    "OpenAIVisionNode": OpenAIVisionNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OpenAIVisionNode": "OpenAI Fashion Analysis"
}