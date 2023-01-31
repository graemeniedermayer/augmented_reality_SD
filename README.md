# Augmented Reality and Stable Diffusion
Combining augmented reality and stability diffusion through api calls.

## Examples
[![video](https://img.youtube.com/vi/_ZFlGsJHMhw/0.jpg)](https://youtu.be/_ZFlGsJHMhw)

## Installation

### local backend setup
#### do on local computer
`git clone https://github.com/graemeniedermayer/augmented_reality_SD.git`

launch automatic1111 with api option (currently it's only setup of 512 models)

`python launch.py --xformers --api`

launch proxy pass server with your private ip address. This can be found with `ip address` linux, `ifconfig` apple or `ipconfig` windows.

`python proxy_pass_server.py --ip 192.168.0.1`

##### optional 
you may want to remake the ssl keys. This is critical if your local network is unsecure for some reason.

`sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout secured-selfsigned.key -out secured-selfsigned.crt`

than change the final lines of proxy_pass_server.py to

`ssl_keyfile='ssl/secured-selfsigned.key',mssl_certfile='ssl/secured-selfsigned.crt'`

`secured-selfsigned.key` is the private key keep it safe.

#### do on android phone
launch [webapp](https://graemeniedermayer.github.io/augmented_reality_SD/frontend/auto1111.html) in portrait mode (I haven't done all the corrections for landscape mode.)

first go to `https://192.168.0.1:8443` (using correct private ip address).

web browser should complain about using an inapproriate certificate. Allow the certificate. This should temporarily allow the self-signed certificate for all browser requests.

`auto1111.html` will contain the default setting. There are going to be a bunch of variants and we'll figure out what works best!

#### do on iOs phone
to do. mozilla webxr mobile viewer might work for some setups (sort of doubt that depth api or camera access will work)

### Cloud Backend
#### google colab
To do

## Using extensions
Many extensions can be very helpful while using augmented reality.

Use full name that would appear in the script area.

## Updates
v 0.0.1 boilerplate

## Setup
So this setup currently requires a front-end, proxy-pass, and back-end.

### Frontend
The current frontend is webxr. Frontend must be hosted with certificate SSL (last time I check self-signed was not sufficient).

Because of the limitations of webxr and iOS I'd like to explore creating a iOS app in the future. 

### Proxy pass
Using a fastapi proxy pass for SSL and cross-site origin resources (CORS) headers. If backend has SSL and CORS enabled this is unnecessary. Automatic1111 supports both but I was having trouble with self-signed certificates. I haven't looked into google Colab yet (it might not be necessary).

### Backend
So far automatic1111 [put link here] is the only backend. I'd like to look into invokeAI and other possible backends.

# Known bugs
* horizontal images does not work.
* must double click capture depth (this is a weird error).
* there is no failure capturing/error capture.

# Useful extensions
[depthmaps](https://github.com/thygate/stable-diffusion-webui-depthmap-script)
[background removal]()

# Acknowledgements 
So many.
To do
