from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict


class ChatRequest(BaseModel):
    message: str
    image_urls: list[str]  # Add image_urls to the request model


class ChatResponse(BaseModel):
    response: str

options = {
    "Image Set 1": [
        "https://www.apple.com/newsroom/images/product/iphone/lifestyle/Apple-Shot-on-iPhone-Challenge-winners-Elizabeth-Scarrott-02262019_big.jpg.large.jpg",
        "https://www.apple.com/newsroom/images/product/iphone/lifestyle/Apple-Shot-on-iPhone-Challenge-winners-Alex-Jiang-02262019_big.jpg.large.jpg",
        "https://www.apple.com/newsroom/images/product/iphone/lifestyle/Apple-Shot-on-iPhone-Challenge-winners-Blake-Marvin-02262019_big.jpg.large.jpg",
        "https://www.apple.com/newsroom/images/product/iphone/lifestyle/Apple-Shot-on-iPhone-Challenge-winners-Darren-Soh-02262019_big.jpg.large.jpg",
    ],
    "Image Set 2": [
        "https://www.apple.com/newsroom/images/product/iphone/lifestyle/Apple-Shot-on-iPhone-Challenge-winners-Nikita-Yarosh-02262019_big.jpg.large.jpg",
        "https://www.apple.com/newsroom/images/product/iphone/lifestyle/Apple-Shot-on-iPhone-Challenge-winners-Dina-Alfasi-02262019_big.jpg.large.jpg",
        "https://www.apple.com/newsroom/images/product/iphone/lifestyle/Apple-Shot-on-iPhone-Challenge-winners-Elizabeth-Scarrott-02262019_big.jpg.large.jpg",
        "https://www.apple.com/newsroom/images/product/iphone/lifestyle/Apple-Shot-on-iPhone-Challenge-winners-Andrew-Griswold-02262019_big.jpg.large.jpg",
    ],
    "Image Set 3": [
        "https://www.apple.com/newsroom/images/product/iphone/lifestyle/Apple-Shot-on-iPhone-Challenge-winners-Bernard-Antolin-02262019_big.jpg.large.jpg",
        "https://www.apple.com/newsroom/images/product/iphone/lifestyle/Apple-Shot-on-iPhone-Challenge-winners-LieAdi-Darmawan-02262019_big.jpg.large.jpg",
        "https://www.apple.com/newsroom/images/product/iphone/lifestyle/Apple-Shot-on-iPhone-Challenge-winners-Robert-Glaser-02262019_big.jpg.large.jpg",
        "https://www.apple.com/newsroom/images/2024/11/apple-debuts-the-weeknds-immersive-music-experience-for-apple-vision-pro/article/Apple-Immersive-Video-The-Weeknd-Open-Hearts_big.jpg.large.jpg",
    ],
}

app = FastAPI()



@app.get("/")
def helloworld():
    return {"Hello": "World"}


@app.get("/images/{image_set}")
def getimageurls(image_set: str):
    try:
        imageUrls = options[image_set]
        return {"image_set": imageUrls}
    except Exception as e:
        print(e)
        print("--- ERROR Retrieving imageUrls. Request received [%s]" % (image_set))
        return {"error": True, "image_set": []}
    
@app.get("/options")
def getoptions():
    keys = []
    for k in options:
        keys.append(k)
    return (keys)

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Handle user messages and return a chatbot response.
    """
    user_message = request.message
    image_urls = request.image_urls

    # Example logic: create a response incorporating the image URLs
    if not user_message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    if "show images" in user_message.lower():
        assistant_message = f"Here are the images you selected:\n" + "\n".join(image_urls)
    elif "hello" in user_message.lower():
        assistant_message = "Hello! How can I assist you today?"
    else:
        assistant_message = "I'm not sure I understand that. Could you please rephrase?"

    # Return the assistant's response
    return ChatResponse(response=assistant_message)