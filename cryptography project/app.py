from flask import Flask, render_template, request

app = Flask(__name__)

def generate_key(plaintext, key):
    key = list(key)
    if len(plaintext) == len(key):
        return "".join(key)
    else:
        for i in range(len(plaintext) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

def encrypt(plaintext, key):
    plaintext = plaintext.upper()
    key = generate_key(plaintext, key.upper())
    ciphertext = ""

    for p, k in zip(plaintext, key):
        if p.isalpha():
            c = (ord(p) - 65 + ord(k) - 65) % 26
            ciphertext += chr(c + 65)
        else:
            ciphertext += p
    return ciphertext

def decrypt(ciphertext, key):
    ciphertext = ciphertext.upper()
    key = generate_key(ciphertext, key.upper())
    plaintext = ""

    for c, k in zip(ciphertext, key):
        if c.isalpha():
            p = (ord(c) - 65 - (ord(k) - 65)) % 26
            plaintext += chr(p + 65)
        else:
            plaintext += c
    return plaintext

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    message = ""
    key = ""
    if request.method == "POST":
        message = request.form.get("message", "")
        key = request.form.get("key", "")
        action = request.form.get("action", "encrypt")

        if action == "encrypt":
            result = encrypt(message, key)
        elif action == "decrypt":
            result = decrypt(message, key)

    return render_template("index.html", result=result, message=message, key=key)

if __name__ == "__main__":
    app.run(debug=True)
