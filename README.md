# ComfyUI OpenAI Vision Node

This custom node for ComfyUI allows you to use OpenAI's GPT-4 Vision model to analyze images within your ComfyUI workflows.

## Installation

You can install this node directly through the ComfyUI Manager using the following Git URL:

```
https://github.com/yourusername/comfyui-openai-vision-node
```

Alternatively, you can manually install it by cloning this repository into your ComfyUI custom nodes directory:

```bash
cd /path/to/ComfyUI/custom_nodes/
git clone https://github.com/yourusername/comfyui-openai-vision-node.git
cd comfyui-openai-vision-node
pip install -r requirements.txt
```

## Usage

1. After installation, restart ComfyUI or reload custom nodes.
2. Look for the "OpenAI Vision Analysis" node in the node menu.
3. Connect an image output to the "image" input of the node.
4. Provide a text prompt describing what you want to analyze or ask about the image.
5. Enter your OpenAI API key.
6. Run your workflow to get the analysis result.

## Note

Keep your API key secure and do not share it publicly. Consider implementing a more secure way of handling the API key in a production environment.

## License

[MIT License](https://opensource.org/licenses/MIT)
