from starlette.requests import Request
from starlette.responses import StreamingResponse
from starlette.background import BackgroundTask
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
import argparse

app = FastAPI()

# there's probably a more elegant way
def getIPaddress():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ipAddress = s.getsockname()[0]
    s.close()
    return ipAddress


# parser
parser = argparse.ArgumentParser(description='starting a proxy pass for automatic1111')
parser.add_argument('-ip', '--ip', default=getIPaddress(), type=str, help='local ip address')
parser.add_argument('-cors', '--cors_origin', type=str, default='https://graemeniedermayer.github.io', help='cors origin')
parser.add_argument('-b', '--backend', type=str, default="http://127.0.0.1:7860/", help='backend for ')

args = parser.parse_args()

# Cross-Origin Resource Sharing Flags
# These flags allow resource from multiple origins to be used.

# Point this to the webxr website origin.
origins = [
    args.cors_origin
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Proxy pass redirect incoming ssl+cors to local server.
import httpx

#pointing to Automatic1111
client = httpx.AsyncClient(base_url=args.backend, timeout=None)

async def _reverse_proxy(request: Request):
    url = httpx.URL(path=request.url.path,
                    query=request.url.query.encode("utf-8"))
    rp_req = client.build_request(request.method, url,
                                  headers=request.headers.raw,
                                  content=await request.body())
    rp_resp = await client.send(rp_req, stream=True)
    return StreamingResponse(
        rp_resp.aiter_raw(),
        status_code=rp_resp.status_code,
        headers=rp_resp.headers,
        background=BackgroundTask(rp_resp.aclose),
    )

# certificate generation
from OpenSSL import crypto, SSL

def cert_gen(
    emailAddress="auto1111webxr@gmail.com",
    commonName="auto1111webxr company",
    countryName="CA",
    localityName="AI",
    stateOrProvinceName="stateOrProvinceName",
    organizationName="auto1111webxr",
    organizationUnitName="auto1111webxr",
    serialNumber=0,
    validityStartInSeconds=0,
    validityEndInSeconds=10*365*24*60*60,
    KEY_FILE = "ssl/selfsigned.key",
    CERT_FILE="ssl/selfsigned.crt"):
    #can look at generated file using openssl:
    #openssl x509 -inform pem -in selfsigned.crt -noout -text
    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = countryName
    cert.get_subject().ST = stateOrProvinceName
    cert.get_subject().L = localityName
    cert.get_subject().O = organizationName
    cert.get_subject().OU = organizationUnitName
    cert.get_subject().CN = commonName
    cert.get_subject().emailAddress = emailAddress
    cert.set_serial_number(serialNumber)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(validityEndInSeconds)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha512')

    with open(KEY_FILE, 'wb+') as f:
        f.write(crypto.dump_privatekey(SSL.FILETYPE_PEM, k))
    with open(CERT_FILE, 'wb+') as f:
        f.write(crypto.dump_certificate(SSL.FILETYPE_PEM, cert))

from pathlib import Path
import os

cert_path = Path("ssl/selfsigned.key")
Path("ssl").mkdir(parents=True, exist_ok=True)
if not cert_path.is_file():
    cert_gen()

app.add_route("/{path:path}",
              _reverse_proxy, ["GET", "POST", "OPTIONS"])
if __name__ == '__main__':
    uvicorn.run(
        'proxy_pass_server:app', port=8443, host=args.ip,
        reload=True, reload_dirs=['./'],
        ssl_keyfile='ssl/selfsigned.key',
        ssl_certfile='ssl/selfsigned.crt')
