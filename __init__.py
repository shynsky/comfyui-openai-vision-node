from .openai_vision_node import OpenAIVisionNode

NODE_CLASS_MAPPINGS = {
    "openai-vlm": OpenAIVisionNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "openai-vlm": "OpenAI VLM"
}