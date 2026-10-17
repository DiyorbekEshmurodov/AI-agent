import os
from mcp.server.fastmcp import FastMCP
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.environ.get("HF_TOKEN")
if not HF_TOKEN:
    raise RuntimeError("Please set HF_TOKEN in .env file")

client = InferenceClient(
    provider="nebius",
    api_key=HF_TOKEN,
)

mcp = FastMCP("ImageGen")


@mcp.tool()
def generate_image(prompt: str, model: str = "black-forest-labs/FLUX.1-schnell") -> str:
    """
    Generate an image from a text prompt using HuggingFace Inference API.
    Return a file path to the saved image. 
    """
    print(f"[ImageGen] Generating image for the prompt: {prompt}")

    out_dir = os.environ.get("OUT_DIR", "outputs")
    os.makedirs(out_dir, exist_ok=True)

    path = os.path.join(out_dir, "image.png")

    image = client.text_to_image(
        prompt,
        model=model,
    )
    image.save(path)

    return path


if __name__ == "__main__":
    mcp.run(transport="stdio")
