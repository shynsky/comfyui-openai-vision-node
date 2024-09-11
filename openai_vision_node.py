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

            # Debug: Print image shape and type
            print(f"Input image shape: {image.shape}, dtype: {image.dtype}")

            # Handle the image format from ComfyUI's "Load Image" node
            if len(image.shape) == 4 and image.shape[0] == 1:
                # Remove the batch dimension
                image = image.squeeze(0)

            # Ensure the image is in the format [height, width, channels]
            if image.shape[2] != 3:
                image = image.permute(1, 2, 0)

            # Convert to numpy and ensure it's in the range 0-255
            image_np = (image.cpu().numpy() * 255).astype(np.uint8)

            # Debug: Print numpy array shape and type
            print(f"Processed numpy array shape: {image_np.shape}, dtype: {image_np.dtype}")

            # Convert to PIL Image
            pil_image = Image.fromarray(image_np)

            # Debug: Print PIL Image size and mode
            print(f"PIL Image size: {pil_image.size}, mode: {pil_image.mode}")

            # Convert the image to base64
            buffered = BytesIO()
            pil_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            prompt = custom_prompt or "Describe in detail, main fashion garment in this image, including its style, color, and notable features.\
            Example: A long, flowy floral print dress with a dark background and colorful flowers in shades of red, pink, purple, and green. High neckline with a small ruffle trim and a crisscross lace-up detail on the chest. Sheer, long sleeves with elastic cuffs and intricate crochet-like detailing along the shoulders. The waist is cinched with a matching fabric belt, creating a fitted look before the skirt flows into a tiered design. The overall look is elegant and romantic, with a bohemian flair."

            payload = {
                "model": "gpt-4o",
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