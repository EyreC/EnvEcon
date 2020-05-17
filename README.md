![Python](https://img.shields.io/badge/python-v3.7-blue.svg)

## Exploring the economic and environmental effects of e-commerce implementation of green delivery schemes
**ECON0052 2019-20 Delivery, Group 1**

**Alexander Craggs, Allysia Dee, Assel Issayeva, Wei Thong, Justin Wong**

A repository for the **agent-based model** developed to explore how agents interact in an economy for e-commerce goods, and how  

---

#### Statistics of the model output

Outputs of the model are saved in .csv files under the `./SavedStats` directory. They are prefixed by their simulation model (benchmark, normal/ simple, and social simulations), and suffixed by whether the output is on the economy level or on the agent level (_simulation and _agent, respectively).  

#### Visualisations of the model output

Visaulisations are done in Jupyter Notebook. They can be found within the `./Visualisations` directory, which is accompanied with Python modules containing visualisation helper functions. 

#### Install Python and dependencies

The application was developed in Python 3.

To install Python code dependencies (outside of Pycharm), the easiest way is using PIP.

`pip install -r requirements.txt`


## Running the app

#### Configurations

The Engine model parameters are inputted in main.py, under Engine inputs. You can tweak the parameters of the Engine, such as number of agents, emissions level of green and normal delivery, and so on here. 

After, you can start the agent-based model simulations by running main.py

`python3 main.py`

If everything is working properly you should see

    Initialising engine
    Initialising agent 0
    Initialising agent 1
    ...

This means that the Engine and Agent classes are being initialised. Upon initialising, you should see

     

model is up has begun its simulations.