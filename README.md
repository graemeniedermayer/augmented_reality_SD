# Augmented Reality and Stable Diffusion
A [webapp](https://graemeniedermayer.github.io/augmented_reality_SD/frontend/auto1111.html) that combines augmented reality and stability diffusion through api calls. Requires running stable diffusion on a seperate machine.

## Examples
[![video](https://img.youtube.com/vi/_ZFlGsJHMhw/0.jpg)](https://youtu.be/_ZFlGsJHMhw)

## Installation

### local backend setup
#### do on local computer
`git clone https://github.com/graemeniedermayer/augmented_reality_SD.git`

launch automatic1111 with api option (currently it's only setup for the 512 models)

`python launch.py --xformers --api`

launch proxy pass server from the project root directory.

`python proxy_pass_server.py`

#### do on android phone
launch [webapp](https://graemeniedermayer.github.io/augmented_reality_SD/frontend/auto1111.html) in portrait mode (I haven't done all the corrections for landscape mode.)

first go to `https://192.168.0.1:8443` (using correct private ip address).

web browser should complain about using an inapproriate certificate. Allow the certificate. This should temporarily allow the self-signed certificate for all browser requests.

`auto1111.html` will contain the default setting. There are going to be a bunch of variants and we'll figure out what works best!

#### do on iOS phone
Todo. mozilla webxr mobile viewer might work for some setups (sort of doubt that depth api or camera access will work)

### Cloud Backend
#### google colab
Todo.

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
So far [automatic1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui) is the only backend. I'd like to look into invokeAI and other possible backends.

# Known bugs
* horizontal images does not work. Resolution changes in general aren't well supported.
* must double click capture depth (this is a weird error).
* there is no failure capturing/error capture.

# Useful extensions
[depthmaps](https://github.com/thygate/stable-diffusion-webui-depthmap-script)

[background removal](https://github.com/graemeniedermayer/clothseg)

# Acknowledgements 
So many.
To do
