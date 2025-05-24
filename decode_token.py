# decode_token.py
import base64
import os

def decode_token():
    secret_path = "/etc/secrets/token_b64.txt"
    output_path = "token.pickle"
    
    if os.path.exists(secret_path):
        with open(secret_path, "r") as f:
            encoded = f.read()
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(encoded))
        print("✅ token.pickle restaurado desde base64")
    else:
        print("❌ token_b64.txt no encontrado en /etc/secrets")

if __name__ == "__main__":
    decode_token()
