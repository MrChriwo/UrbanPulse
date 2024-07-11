import os 

from sumo_rl import parallel_env, env 

PATH = os.path.dirname(os.path.realpath(__file__))


def darmstadt_env(parallel=True, **kwargs):
    """Darmstadt Enviornment.

    Number of agents: 3
    Number of actions: 2 agents with 4 actions and 1 agent with 3 actions
    2 agents have the same observation and action space and 1 has different spaces
    """
    kwargs.update(
        {
            "net_file": PATH + "\\config\\darmstadt.net.xml",
            "route_file": PATH + "\\config\\darmstadt.rou.xml",
            "begin_time": 3,
            "num_seconds": 2996 - 2,
        }
    )
    if parallel:
        return parallel_env(**kwargs)
    else:
        return env(**kwargs)
    

if __name__ == "__main__":
    env = darmstadt_env()
    observations = env.reset()
    print("done")	