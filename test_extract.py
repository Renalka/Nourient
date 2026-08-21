import requests

try:
    # We just need a dummy image to trigger the API. We can use a random small file from the system or create one.
    with open("test.jpg", "wb") as f:
        f.write(b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.' \",#\x1c\x1c(7),01444\x1f'9=82<.342\xff\xd9")
    
    with open("test.jpg", "rb") as f:
        resp = requests.post("http://localhost:8000/api/v1/vision/extract", files={"file": ("test.jpg", f, "image/jpeg")})
    print("Status:", resp.status_code)
    print("Response:", resp.text)
except Exception as e:
    print(e)
