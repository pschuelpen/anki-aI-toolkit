# Anki AI Toolkit ⭐ - AI Cards generation & Package management

![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![image](https://img.shields.io/badge/ChatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)

The Anki Toolkit is meant for automatic card generation from PDF Files. Imagine the Situation: You get a lot of material from your courses in the form of pdf's and while starting to study you realize that you cant afford the time to read through all of them but still you dont want to miss information.

Some Tools like this already exist YES but most of them are expensive. This Toolkit only needs you to use the OpenAI API (purchase of API credits required) or install a local model like Ollama to use local LLM's. Its open source therefore you can definetly customize functionality, optimize promts and keep your files by yourself

>Warning! Text data will be transmitted to OpenAI if ChatGPT API is being used !! This might be relevant to you if privacy is your concern. For private use please use Ollama locally

## 🤖 OpenAI API - important Information !!

> If you plan on using ChatGPT to create your Anki Cards please read this abstract!

### 💸 Costs

Using OpenAI can also be quiet costly to use in the long term. For current pricing please go to OpenAI's Website for reference. Depending on the Size of your documents or the amount of requests you cold expect to pay a bunch for using the API. Although you pay some money you as much requests as you want as long as you pay the API Credits. You can also use the Credits for alternative use of ChatGPT in other Scripts, Programs or Projects from Github even. So there is definetly a benifit. Just be aware of the Price and that using **OpenAI's Service is not Free**

### 🔒 Privacy

Using an API to share Document Data is **Always** a risky thing in general. Be aware of that all the time anyway!! But for the sake of this project oin particular you might come across the choice of using documents with copyright protection or certain classifications. Be aware of the Security Risks providing an external Service provider your Data for Free!! 

If you have Documents not worth sharing please dont use the Tool for that! An Ollama integration is on its way, able to compute similar results locally without a privacy concern!

### ⚙️ Using OpenAI API - Setup Required

To Use ChatGPT in the Toolkit you need to generate your `config.yaml` file first! Please do that in advance of first use! 

```shell
./setup.sh -e "API-KEY"
```

After successful generation of the Config File you can start the Program !



## 🌐 Usage Explained

Running the Program in Docker simplifies execution and package management. If possible please use docker since we only use the Docker image for development. Since Docker runs perfetly on a RaspberryPi I'd recommend installing it there if you dont have a different alternative. It works perfectly on RPi4 and RPi5 (I could only test those). If using Docker is not possible, a virtual enviroment would work too, but requires additional Setup and may be painful. 

### 🐳 Docker - Recommended

I havent uploaded to DockerHub yet therefore you need to Clone the Repo and build the Container yourself

#### 1. Build the Container

To build the Docker container please use this command:

```shell
sudo docker build -t anki_ai_toolkit .
```

#### 2. Run the Container

Run the Docker container that siply runs once like that **when in the main directory of the Repo (otherwise adjust the paths)**:

```shell
sudo docker run -it --rm \
  -v ./src:/usr/app/src \
  -v ./resources:/usr/app/resources \
  anki_ai_toolkit
```

#### Files

Place your files inside the `/resources/pdf` Folder and get your Anki Decks inside the `/resources/anki` Folder

### 🤓 Virtual Enviroment - not recommended but would work too

If Docker is unable to be used you can use virtual enviroments aswell. Simply create the enviroment like this using the `env` Name and install the packages:

```shell
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```

To run the Scripts go to the `src` Folder and run the python script:

```shell
python3 main.py
```

> Warning :: You have to change Paths in the `main.py` Script to manually use the Script. Program is build to run in Docker therefore they are hardcoded to fit the Containers Volumes


## ☝️ Additional

### 🙋🏼‍♂️ personal Opinion

The Toolkit proves to be better than expected to be honest. Still to create the Perfect Anki Cards I'd personally recommend to personally work for it too! AI is great in writing and great in summarizing, but most of the time it's unable to focus on personally focus on what you specifically need for studying and obviosly it can't predict how you study best! Improvements can be made for shure, but currently This tool was not perfected **yet**. Some improvements still to come! 

To conclude my personal opignion: I think it's a great Tool to start with a Deck, but addiotional Work has to be done with Fact-Checking (to be shure) and optimizing to your personal needs. After all doing something to study effectively pays off and you want to make shure that what you study is actually correct!!

### 🚀 Future Features

- [x] Working Version with OpenAI API
- [ ] Integrate Ollama for local LLM Requests (privacy)
- [ ] Ability to extract Cards from existing Stacks
- [ ] Ability to extend existing Decks
- [ ] Build better Assistant for Anki Cards - Promt Engineering
- [ ] Push Docker Container to DockerHub
- [ ] Build WebUI - Transfer to Web usage rather than Terminal
- [ ] Automated Routines for Courses - Automatic Extention of decks from new PDF's of your course
- [ ] ? Train custom LLM optimized for Anki Cards (unlikely at this point but maybe in the Future)

### 🤷🏼‍♂️ About

Code written by Philipp Schülpen, pschuelpen 2025

This doesn't have any relation to the official ANKI - But I recommend checking them out they are Great!!

### 🔗 Links

- 🔗[Official Anki Repository](https://github.com/ankitects/anki)
- 🔗[GenAnki Repository](https://github.com/kerrickstaley/genanki)


