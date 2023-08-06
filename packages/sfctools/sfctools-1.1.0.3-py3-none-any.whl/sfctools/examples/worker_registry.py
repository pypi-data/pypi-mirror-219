__author__ = "Thomas Baldauf"
__email__ = "thomas.baldauf@dlr.de"
__license__ = "MIT"
__birthdate__ = '23.06.202'
__status__ = 'dev' # options are: dev, test, prod

from sfctools.examples.example_wrapper import Example

from sfctools.datastructs.worker_registry import WorkerRegistry
from sfctools import Agent
import numpy as np
np.random.seed(1980)

def run():

    class Worker(Agent):
        def __init__(self):
            super().__init__()
            self.reservation_wage = np.random.rand()

    a = Agent()

    wreg = WorkerRegistry(owner=a,wage_attr="reservation_wage") # create a new worker registry
    workers = [Worker() for i in range(10)] # create a bunch of workers

    for worker in workers: # add workers to registry
        wreg.add_worker(worker)
    
    costs = wreg.get_avg_costs() # get average reservation wage of all workers
    print("Average cost: %.2f\n" % costs)

    wreg.fire_random(2) # fire two random workers

    # pop workers from the worker stack
    print("Wokers left:")
    for i in range(8):
        print(wreg.pop())
    

class WorkerExample(Example):
    def __init__(self):
        super().__init__(run)


if __name__ == "__main__":
    my_instance = WorkerExample()
    my_instance.run()