# 4 Easy Ways for Network Engineers to Go from an Un-Programmed to an Automated Network
Supplementary material for the Cisco Live EMEA 2023 session BRKOPS-2717.

## 4 easy ways towards automated network
* [Way 2](Way2)
* [Way 3](Way3)
* [Way 4](Way4)
* [Getting started](GetStarted)

## Before you start
All of the code presented in the Cisco Live session is available for you on this Github repository. If you do not have programming experience before hand, there are couple of steps you will need to cover before you can start trying the examples out.

### Prepare your developer environment
- Install Python version 3
- Install Git
- Install a code editor, for example Visual Studio Code

Not sure how to do these? DevNet has great learning material to get you through these steps. You will need a free DevNet account to access the material, so register [here](https://developer.cisco.com/) if you haven't, and enjoy the learning labs to get your developer environment started:

* Windows: https://developer.cisco.com/learning/modules/dev-setup/dev-win/step/1
* Mac: https://developer.cisco.com/learning/modules/dev-setup/dev-mac/step/1
* Linux (CentOS): https://developer.cisco.com/learning/modules/dev-setup/dev-centos/step/1
* Linux (Ubuntu): https://developer.cisco.com/learning/modules/dev-setup/dev-ubuntu/step/1

### Clone the repository and install required libraries
When you have your developer environment up and running, make sure you install all libraries and modules required for your scripts. To keep your developer environment tidy, make sure to activate your virtual environment before installing the libraries.

Clone this repository to the environment in which your are working:
```bash
git clone https://github.com/juuliasantala/BRKOPS-2717.git
```

Install the requirements to have all the necessary libraries for the code examples to work.

```bash
pip install -r requirements.txt 
```

## Authors & Maintainers
People responsible for the creation and maintenance of this project:
* Christina Skoglund cskoglun@cisco.com
* Juulia Santala jusantal@cisco.com

## License
This project is licensed to you under the terms of the [Cisco Sample Code License](LICENSE).
