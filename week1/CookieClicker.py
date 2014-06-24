"""
Cookie Clicker Simulator
"""

#import simpleplot

# Used to increase the timeout, if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        """
            Init the ClickerState.
        """
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._total_cookies = 0.0
        self._current_cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return str([self._current_time, self._current_cookies, \
            self._current_cps, self._total_cookies])
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        return _get_time_until(self._current_cookies, \
            self._current_cps, cookies)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time <= 0:
            return
        cookie_produced = time * self._current_cps
        self._current_time += time
        self._current_cookies += cookie_produced
        self._total_cookies += cookie_produced
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        And change history (time, item, cost of item, total cookies)
        """
        if self._current_cookies < cost:
            return
        self._current_cookies -= cost
        self._current_cps += additional_cps
        self._history.append((self._current_time, item_name, \
            cost, self._total_cookies))

def _get_time_until(current_cookies, cps, cookies):
    """
        Return time until you have the given number of cookies
    """
    if current_cookies >= cookies:
        return 0.0
    cookies -= current_cookies
    wait_time = cookies / cps
    remain = wait_time - round(wait_time)
    if remain != 0.0:
        if remain < 0:
            wait_time = round(wait_time)
        else:
            wait_time = round(wait_time)+1
    return wait_time + 0.0  
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    state = ClickerState()
    info = build_info.clone()
    while state.get_time() <= duration:
        remain_time = duration - state.get_time()
        item = strategy(state.get_cookies(), state.get_cps(),\
         remain_time, info)
        if item is None:
            state.wait(remain_time)
            break
        cost = info.get_cost(item)
        additional_cps = info.get_cps(item)
        time_wait = state.time_until(cost)
        if time_wait > remain_time:
            state.wait(remain_time)
            break
        state.wait(time_wait)
        state.buy_item(item, cost, additional_cps)
        info.update_item(item)
    return state


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    dummy_cookies = cookies
    dummy_cps = cps
    dummy_time_left = time_left
    dummy_info = build_info
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    dummy_cookies = cookies
    dummy_cps = cps
    dummy_time_left = time_left
    dummy_info = build_info
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
        this strategy should always select the cheapest item.
    """
    dummy_cookies = cookies
    dummy_cps = cps
    dummy_time_left = time_left
    all_items = build_info.build_items()
    def sort_by_price(item):
        """
            sort function for cheap.
        """
        return build_info.get_cost(item)
    all_items = sorted(all_items, key=sort_by_price)
    total_cookies = cookies + cps * time_left
    for item in all_items:
        if build_info.get_cost(item) <= total_cookies:
            return item
    return None

def strategy_expensive(cookies, cps, time_left, build_info):
    """
        this strategy should always select the most expensive item 
        you can afford in the time left.
    """
    total_cookies = cookies + cps * time_left
    select_item = None
    all_items = build_info.build_items()
    for item in all_items:
        if build_info.get_cost(item) <= total_cookies:
            if select_item is None:
                select_item = item
            elif build_info.get_cost(item) > build_info.get_cost(select_item):
                select_item = item
    return select_item

def strategy_best(cookies, cps, time_left, build_info):
    """
        this is the best strategy that you can come up with.
    """
    all_items = build_info.build_items()
    def max_cps_cost(item):
        """
            used for compare item.
        """
        return build_info.get_cps(item) / build_info.get_cost(item)
    all_items = sorted(all_items, key=max_cps_cost, reverse=True)
    total_cookies = cookies + cps * time_left
    for item in all_items:
        if build_info.get_cost(item) < total_cookies:
            return item
    return None
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    #state = simulate_clicker(provided.BuildInfo(), time, strategy)
    state = simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 50.0]}, 1.15), 16, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    print history
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def _get_build_info():
    """
        get the item informations.
    """
    info = provided.BuildInfo()
    all_items = info.build_items()
    for item in all_items:
        print item, info.get_cps(item) / info.get_cost(item)

def run():
    """
    Run the simulator.
    """   
    # _get_build_info()
    run_strategy("Cursor", SIM_TIME, strategy_cursor)

    # Add calls to run_strategy to run additional strategies
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    #run_strategy("Best", SIM_TIME, strategy_best)
    
run()
