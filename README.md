# Augmented Reality and Stable Diffusion
Combining augmented reality and stability diffusion through api calls.

## Installation
### local backend setup
#### do on local computer
`git clone https://github.com/graemeniedermayer/augmented_reality_SD.git`

launch automatic1111 with api option
`python launch.py --xformers --api`

launch proxy pass server with your private ip address
`python proxy_pass_server.py --ip 192.168.0.1`

optional: you may want to remake the ssl keys. This is critical if your local network is unsecure for some reason.
`sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout secured-selfsigned.key -out secured-selfsigned.crt`

`secured-selfsigned.key` is the private key.

#### do on mobile phone
launch webapp [cite]

first go to `https://192.168.0.1:8443` (using correct private ip address).

web browser should complain about using an inapproriate certificate. Allow the certificate. This should temporarily allow the self-signed certificate for all browser requests.

### colab setup
To do

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

# Useful extensions
depth

# Acknowledgements 
So many.
