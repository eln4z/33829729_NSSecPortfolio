import pyotp, qrcode

def generate_2fa_secret(username: str):
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)

    uri = totp.provisioning_uri(name=username, issuer_name="NSSecDemoApp")

    img = qrcode.make(uri)
    filename = f"totp_{username}.png"
    img.save(filename)

    return secret, filename
