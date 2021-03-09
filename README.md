# "Robo-Advisor" Project
A tool to automate the process of providing business clients with stock trading recommendations. The program accepts one or more stock or cryptocurrency symbols as information inputs, then it requests real live historical trading data from the Internet, and finally it provides a recommendation as to whether or not the client should purchase the given stocks or cryptocurrencies.

## Project Description
Published by Professor Michael Rossetti vis a vis github accessable [here](https://github.com/prof-rossetti/intro-to-python/blob/master/projects/robo-advisor/README.md "here").

Issues requests to the [AlphaVantage Stock Market API](https://www.alphavantage.co/ "AlphaVantage Stock Market API") in order to provide automated stock or cryptocurrency trading recommentdations.


## Prerequisites
+  Command-Line Application (Terminal or Git Bash)
+  Python Installation (3.7+)
+  Pip

## Installation
Clone or download from [Github Source](https://github.com/antoniogriffith/Shopping-Cart "Github Source"), then navigate into the project repository from the command-line application:

Ensure that you are aware where the repository has been saved locally:

```sh
cd Robo-Advisor
```
### Environmental Setup

Use Anaconda to create and activate a new virtual environment, perhaps named "stocks-env". 

'''sh
conda create -n stocks-env python=3.8
conda activate stocks-env
'''

From inside the virtual environment, install packages specified in the "requirements.txt" file
'''sh
pip install -r requirements.txt
'''

#### API Setup

Visit Alpha Vantage's website at this [link](https://www.alphavantage.co/support/#api-key, "link") and obtain an API Key.

Create a new file in this repository called .env and place inside the following contents:

'''sh
ALPHAVANTAGE_API_KEY = "___________"
'''

## Usage

From within the virtual environment, demonstrate your ability to run the Python script from the command-line:

'''sh
python app/robo_advisor.py
'''

Once the program is running, follow the on-screen instructions.