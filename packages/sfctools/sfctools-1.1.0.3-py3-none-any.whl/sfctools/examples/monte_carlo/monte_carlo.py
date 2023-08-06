from sfctools.automation.runner import ModelRunner
from sfctools import Settings, World, Agent
import numpy as np
np.random.seed(1235)
import pandas as pd
import os 

"""
This tests the automation routines for monte-carlo batches
"""

from sfctools.examples.example_wrapper import Example


def run(base_path):
    # run this in the upper directory via pytest tests/, otherwise this will fail


    # run this in the upper directory via pytest tests/, otherwise this will fail
    settings_path = os.path.join(base_path, "testsettings.yml")
    results_path = os.path.join(base_path, "results/")

    # run this in the upper directory via pytest tests/, otherwise this will fail

    class MyAgent(Agent):
        def __init__(self):
            super().__init__()
            self.a_param = Settings()["param_a"]

        def modify_a(self):
            self.a_param *= np.random.rand()

    def builder():
        # placeholder for agent builder, 
        my_agents = [MyAgent() for i in range(10)]
            

    def iter(n): # one model iteration, repeated n times
        my_agents = World().get_agents_of_type("MyAgent")

        vals = []
        for i in range(n):
            # write agents' parameters here (just an example)
            [agent.modify_a() for agent in my_agents]
            a_param_vals = [agent.a_param for agent in my_agents]
            vals.append(np.mean(a_param_vals))

        return pd.DataFrame({"Value":vals}) # has to return a dataframe

    # create model runner
    print("settings path", settings_path)
    mr = ModelRunner(settings_path,results_path,builder,iter)
    mr.run(10,20)

    # read back the output files
    with open(os.path.join(results_path, "output.txt"), "r") as file:
        print("1. output.txt:\n ", file.readlines()[:3], "\n")

    with open(os.path.join(results_path, "progress.txt"), "r") as file:
        print("2. progress.txt:\n ", file.readlines()[:3], "\n")

    with open(os.path.join(results_path, "output.0"), "r") as file:
        print("3. values:\n ", file.readlines()[:3], "\n")



class MonteCarloExample(Example):
    def __init__(self, base_path = None, settings_path = None, results_path = None):

        # assign default paths 
        if base_path is None:
            base_path = "sfctools/examples/monte_carlo/"

        super().__init__(lambda : run(base_path))


if __name__ == "__main__":

    base_path = os.getcwd()
    mc_ex = MonteCarloExample(base_path) 
    mc_ex.run()