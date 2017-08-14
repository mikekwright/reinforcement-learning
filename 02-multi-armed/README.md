k-Armed Bandit
=================================

So what is a _k-Armed Bandit_ problem...  

Consider the following learning problem. You are faced repeatedly with a choice among k di↵erent options,
or actions. After each choice you receive a numerical reward chosen from a stationary probability
distribution that depends on the action you selected. Your objective is to maximize the expected total
reward over some time period, for example, over 1000 action selections, or time steps.    

    # Note: This is an approximation 
    q⇤(a) = E[ Rt | At=a ]

    # E[X] -> Expectation of random variable X
    # Rt -> Reward at Time t
    # At -> Actions at Time t

