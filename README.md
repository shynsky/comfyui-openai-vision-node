# ComfyUI OpenAI Fashion Analysis Node

This custom node for ComfyUI allows you to use OpenAI's GPT-4 Vision model to analyze fashion garments in images within your ComfyUI workflows.

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
2. Look for the "OpenAI Fashion Analysis" node in the node menu.
3. Connect an image output to the "image" input of the node.
4. Enter your OpenAI API key in the "api_key" field.
5. (Optional) Customize the analysis prompt or adjust the maximum number of tokens for the response.
6. Run your workflow to get the fashion analysis result.

## Input Parameters

- `image`: The input image to analyze (required)
- `api_key`: Your OpenAI API key (required)
- `custom_prompt`: A custom prompt for the analysis (optional, default provided)
- `max_tokens`: Maximum number of tokens for the response (optional, default: 300)

## Output

The node outputs a string containing the fashion analysis of the main garment in the image.

## Note

Keep your API key secure and do not share it publicly. Consider implementing a more secure way of handling the API key in a production environment.

## License

[MIT License](https://opensource.org/licenses/MIT)