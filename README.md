# Install Notes

Given an input phrase, this project asks the Llama-2-7B LLM AI model to generate one or more synonyms of each word. Then with each synonym, it generates a new phrase by replacing each word. Finally with each new phrase it asks the model to rephrase it, and all the new phrases are returned.


[[_TOC_]]

## Developer Environment Setup

To get started with development, you will need to have cloned this repo to your computer.

### Pre-requisites

- Amazon EC2 Instance with GPU, g4dn.xlarge with 30GB storage minimum.
- Linux Host or WSL on a Windows machine.
- Not tested on Mac, but it should be the same.


### Create an EC2 Instance with GPU

g4dn.xlarge
4 vCPU 16 GiB Memory
GPU: NVIDIA Corporation TU104GL [Tesla T4] (rev a1)
https://www.techpowerup.com/gpu-specs/tesla-t4.c3316
https://www.techpowerup.com/gpu-specs/nvidia-tu104.g854#:~:text=It%20features%203072%20shading%20units,contains%2048%20raytracing%20acceleration%20cores.
16GB DDR6 - Memory Bus 256 bit - Bandwidth 320.0 GB/s - 585 MHz

Storage: 100 GiB General purpose SSD (gp3)
OS: Ubuntu Server 22.04.4 LTS (Jammy Jellyfish) 64-bit (x86)

Software Image (AMI)
Canonical, Ubuntu, 22.04 LTS, amd64 jammy image build on 2024-03-01
ami-0b8b44ec9a8f90422

Generate a key pair and download your public key.

Start your EC2 instance and copy the Public DNS address.


### Connect to EC2 Instance

Copy your public key to your target folder (llama2_key.pem)

```
sudo chmod 400 llama2_key.pem
sudo ssh -i "llama2_key.pem" ubuntu@EC2_Public_DNS
```

Example:
```
sudo ssh -i llama2_key.pem ubuntu@ec2-18-223-107-29.us-east-2.compute.amazonaws.com
```
(From WSL sudo is required to run ssh)


### Setup Target Environment

```
sudo apt-get update
sudo apt -y install python3 python3-dev python3-pip python3-virtualenv gcc build-essential git libffi-dev
python3 -m pip install --upgrade pip

virtualenv llama_env
source llama_env/bin/activate
```

### Register and Download Llama2

Visit the Meta website and register to download the model/s.:
https://llama.meta.com/llama-downloads/

```
git clone https://github.com/meta-llama/llama.git
cd llama
```

Once registered, you will get an email with a URL to download the models. You will need this URL when you run the download.sh script:
```
./download.sh
```
--> Input: 7B-chat


### Install packages

```
pip install -e .
```

### Test CUDA is available with torch library

<pre>
  <code class="language-python">
python
Python 3.8.10 (default, Nov 26 2021, 20:14:08)
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> torch.cuda.is_available()
False
>>> torch._C._cuda_getDeviceCount()
0
>>>
  </code>
</pre>


### Install Nvidia Driver

```
sudo /sbin/update-pciids
lspci | grep -i nvidia
00:1e.0 3D controller: NVIDIA Corporation TU104GL [Tesla T4] (rev a1)

sudo apt install ubuntu-drivers-common
sudo apt install alsa-utils
sudo ubuntu-drivers devices
== /sys/devices/pci0000:00/0000:00:1e.0 ==
modalias : pci:v000010DEd00001EB8sv000010DEsd000012A2bc03sc02i00
vendor   : NVIDIA Corporation
model    : TU104GL [Tesla T4]
driver   : nvidia-driver-550-server - distro non-free
driver   : nvidia-driver-545 - distro non-free
driver   : nvidia-driver-550 - distro non-free recommended
driver   : nvidia-driver-535 - distro non-free
driver   : nvidia-driver-418-server - distro non-free
driver   : nvidia-driver-450-server - distro non-free
driver   : nvidia-driver-470-server - distro non-free
driver   : nvidia-driver-470 - distro non-free
driver   : nvidia-driver-535-server - distro non-free
driver   : xserver-xorg-video-nouveau - distro free builtin

→ driver   : nvidia-driver-550 - distro non-free recommended

sudo apt install nvidia-driver-550
```

### Reboot Instance

```
sudo halt
→ Stop Instance
→ Start Instance
```

### Connect to EC2 Instance

```
sudo ssh -i "llama2_key.pem" ubuntu@Public_DNS
```


### Test CUDA is available with torch library

```
cd /home/ubuntu/$YOUR_PATH/llama
source llama_env/bin/activate
```

<pre>
  <code class="language-python">
(llama_env) ubuntu@ip-172-31-7-235:~/IA/llama-2/llama$ python
Python 3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> torch.cuda.is_available()
True
>>> torch._C._cuda_getDeviceCount()
1
>>>
  </code>
</pre>


### Run the model locally

```
chmod +x rephrase_ai.sh
./rephrase_ai.sh
```


### Sample Test


```
🦙 Enter an english phrase:  you are the best

💬 [Rephrase] ------------>  You stand out from the crowd.

💬 [Rephrase] ------------>  You are truly unique.

💬 [Rephrase] ------------>  You are an individual with your own special qualities.

💬 [Rephrase] ------------>  You are one of a kind.

💬 [Rephrase] ------------>  You are extraordinary.

💬 [Rephrase] ------------>  You are a rare find.

💬 [Rephrase] ------------>  You are a breath of fresh air.

💬 [Rephrase] ------------>  You are a shining star.

💬 [Rephrase] ------------>  You are a cut above the rest.

💬 [Rephrase] ------------>  You are a true original.

💬 [Rephrase] ------------>  You are exceptional.

💬 [Rephrase] ------------>  You are remarkable.

💬 [Rephrase] ------------>  You are impressive.

💬 [Rephrase] ------------>  You are outstandingly talented.

💬 [Rephrase] ------------>  You are truly remarkable.

💬 [Rephrase] ------------>  You are an exceptional individual.

💬 [Rephrase] ------------>  You are a standout.

💬 [Rephrase] ------------>  You are a cut above the rest.

💬 [Rephrase] ------------>  You are an extraordinary person.

💬 [Rephrase] ------------>  You are a remarkable individual.

💬 [Rephrase] ------------>  You are truly remarkable.

💬 [Rephrase] ------------>  Your exceptional qualities are truly remarkable.

💬 [Rephrase] ------------>  You have an incredible talent for being remarkable.

💬 [Rephrase] ------------>  Your dedication and hard work make you truly remarkable.

💬 [Rephrase] ------------>  You are an inspiration to be around, your remarkable qualities are evident in everything you do.

💬 [Rephrase] ------------>  Your remarkable abilities and achievements are a testament to your hard work and dedication.

💬 [Rephrase] ------------>  You have a unique gift for making a difference, your remarkable qualities are evident in everything you do.

💬 [Rephrase] ------------>  You are a remarkable individual, your talents and abilities are truly exceptional.

💬 [Rephrase] ------------>  Your remarkable qualities are what make you stand out from the crowd.

💬 [Rephrase] ------------>  You have a remarkable ability to inspire and motivate others.

💬 [Rephrase] ------------>  Your remarkable qualities are a reflection of your passion and dedication.

💬 [Rephrase] ------------>  People are the best.

💬 [Rephrase] ------------>  Individuals are the best.

💬 [Rephrase] ------------>  Humans are the best.

💬 [Rephrase] ------------>  Folks are the best.

💬 [Rephrase] ------------>  Folk are the best.

💬 [Rephrase] ------------>  Each person has their own unique strengths and abilities, making them an invaluable asset to any team or organization.

💬 [Rephrase] ------------>  The diversity of individuals is what makes a group or team truly exceptional, as each person brings their own set of skills and perspectives to the table.

💬 [Rephrase] ------------>  Individuality is what drives innovation and progress, as people are encouraged to think outside the box and bring their own ideas to the table.

💬 [Rephrase] ------------>  The strength of a group lies in the diversity of its members, as each person brings their own unique experiences and talents to the table.

💬 [Rephrase] ------------>  By valuing and embracing individuality, organizations can tap into the collective potential of their employees, leading to greater creativity, productivity, and success.
```


### Check GPU usage while running the model

On another terminal run:

```
nvidia-smi
Thu Apr 11 16:13:15 2024
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 550.67                 Driver Version: 550.67         CUDA Version: 12.4     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  Tesla T4                       Off |   00000000:00:1E.0 Off |                    0 |
| N/A   37C    P0             68W /   70W |   14033MiB /  15360MiB |     99%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|    0   N/A  N/A      1754      C   .../llama-2/llama/llama_env/bin/python      14030MiB |
+-----------------------------------------------------------------------------------------+
```
