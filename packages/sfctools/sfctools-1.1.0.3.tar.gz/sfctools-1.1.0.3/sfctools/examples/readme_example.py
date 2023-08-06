
from sfctools.automation.runner import ModelRunner
from sfctools import Agent,World


from sfctools.examples.example_wrapper import Example



def run():
        
    class SomeAgent(Agent):
        def __init__(self, a):
            super().__init__()
            self.some_attribute = a
    
    my_agent = SomeAgent(a='Hello')
    your_agent = SomeAgent(a='World')
    
    my_agents = World().get_agents_of_type("SomeAgent")
    my_message = my_agents[0].some_attribute
    your_message = my_agents[1].some_attribute

    print("%s says %s, %s says %s" % (my_agent, my_message, your_agent, your_message))



class ReadMeExample(Example):
    def __init__(self):
        super().__init__(lambda: run)
    


if __name__ == "__main__":
    ReadMeExample().run()