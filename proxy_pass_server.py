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

# parser
parser = argparse.ArgumentParser(description='starting a proxy pass for automatic1111')
parser.add_argument('-ip', '--ip', default='192.168.0.1', type=str, help='local ip address')
parser.add_argument('-cors', '--cors_origin', type=str, default='https://graemeniedermayer.github.io', help='cors origin')
parser.add_argument('-b', '--backend', type=str, default="http://127.0.0.1:7860/", help='backend for ')

args = parser.parse_args()

# Cross-Origin Resource Sharing Flags
# These flags allow resource from multiple origins to be used.

# Point this to the webxr website origin.
origins = [
    args.indir
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
client = httpx.AsyncClient(base_url="http://127.0.0.1:7860/", timeout=None)

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

from pathlib import Path

app.add_route("/{path:path}",
              _reverse_proxy, ["GET", "POST", "OPTIONS"])
if __name__ == '__main__':
    uvicorn.run(
        'proxy_pass_server:app', port=8443, host=args.ip,
        reload=True, reload_dirs=['./'],
        ssl_keyfile='ssl/unsecure-selfsigned.key',
        ssl_certfile='ssl/unsecure-selfsigned.crt')
