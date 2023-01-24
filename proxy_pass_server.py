from starlette.requests import Request
from starlette.responses import StreamingResponse
from starlette.background import BackgroundTask
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import FastAPI
from starlette.requests import Request

app = FastAPI()

# Cross-Origin Resource Sharing Flags
# These flags allow resource from multiple origins to be used.

# Point this to the webxr website origin.
origins = [
    "https://"]

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

# check for ssl keys and create if they don't exist
# if not (Path("fast-selfsigned.key").is_file() and Path("fast-selfsigned.crt").is_file()):
#     # generate ssl certificates
#     from Cryptodome.PublicKey import RSA
#     key = RSA.generate(2048)
#     pv_key_string = key.exportKey()
#     with open ("fast-selfsigned.key", "w") as prv_file:
#         print("{}".format(pv_key_string.decode()), file=prv_file)

#     pb_key_string = key.publickey().exportKey()
#     with open ("fast-selfsigned.crt", "w") as pub_file:
#         print("{}".format(pb_key_string.decode()), file=pub_file)

app.add_route("/{path:path}",
              _reverse_proxy, ["GET", "POST", "OPTIONS"])
if __name__ == '__main__':
    uvicorn.run(
        'proxy_pass:app', port=8443, host='192.168.0.1',
        reload=True, reload_dirs=['./'],
        ssl_keyfile='fast-selfsigned.key',
        ssl_certfile='fast-selfsigned.crt')
