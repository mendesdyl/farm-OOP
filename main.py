from typing import List

class Cow:
    def __init__(self, breed: str, feed_type: str, milk_yield: int, greenhouse_gas: int):
        # Set all the variables used for each cow. These can be called later in other methods. 
        self.breed = breed
        self.feed_type = feed_type
        self.milk_yield = milk_yield
        self.greenhouse_gas = greenhouse_gas

class Pen:
    def __init__(self, pen_id: str, max_cows: int):
        # Set all the variables used for each pen. 
        self.pen_id = pen_id
        self.max_cows = max_cows
        self.cows = []
        self.breed = 'none'

    def add_cow(self, cow: Cow) -> bool:
        if self.breed == 'none' or cow.breed == self.breed:
            # Make sure this pen instance has no breed or the breed you are trying to add matches the breed in the pen.
            if len(self.cows) < self.max_cows:
                # If the max number of cows is not reached then add the cow to the pen.
                self.cows.append(cow) # Add cow to pen.
                self.breed = cow.breed # Sets the breed of the pen from the first cow or subsequent cows enter the pen.
                return True     # True the cow has been allocated.
            else:
                return False
                # If max number of cows reached return False.
        else:
            return False
            # Return False if the breed does not match aka try another pen.

    def remove_cow(self, cow: Cow) -> bool:
        if cow in self.cows:
            # If cow is in the pen instance then proceed.
            self.cows.remove(cow) # Remove the cow 
            if len(self.cows) == 0:
                # If there are no cows then set the breed back to none.
                self.breed = 'none'   
            return True     
            # Return True for a cow sucessfully removed.
        return False       
        # Return False the cow could not be removed for some reason.

class Farm:
    def __init__(self, pens: List[Pen]):
        # Set the variable used for a farm.
        self.pens = pens

    def allocate_cows(self, cows: List[Cow]) -> bool:
        for cow in cows:
            # For every cow in the list of cows you want to allocate.
            # Set the allocation of each cow to False.
            allocated = False
            while not allocated: # Self-explanatory.
                for pen in self.pens:
                    # Start with the first pen you have avilable on this farm and loop through until...
                    if pen.add_cow(cow):
                        # Try to add cow to the pen, True if the cow was allocated, and False if the cow was not allocated.
                        allocated = True
                        break   
                        # Break out of the for loop once cow is allocated.
            if not allocated:
                # If the cow was not allocated return False on the allocate cows method.
                return False
        return True
        # If all cows were sucessfully allocated then return True.

    def calculate_milk_yield(self) -> dict:
        milk_yield_data = {pen.pen_id: [] for pen in self.pens}
        # Create an empty dictionary to store the milk yield data for each pen. 
        for pen in self.pens:
            # Loop through all of the pens on the farm.
            milk_yield = sum([cow.milk_yield for cow in pen.cows])
            # Calculate the milk yield for all of the cows in a pen.
            milk_yield_data[pen.pen_id].append(milk_yield)
            # Add milk yield data to the dictionary and return the dictionary.
        return milk_yield_data

    def greenhouse_gas_emissions(self) -> int:
        greenhouse_gas = sum([cow.greenhouse_gas for pen in self.pens for cow in pen.cows])
        # Add all of the greenhouse emissions for each cow in each pen on the farm and return the resulting integer.
        return greenhouse_gas

    def estimate_cost(self, feed_prices: dict) -> float:
        feed_costs = {feed_type: 0 for feed_type in feed_prices}
        # Create an empty dictionary to store the feed costs for each feed type.
        for pen in self.pens:
            # For each pen on the farm...
            for cow in pen.cows:
                # For each cow in each pen...
                feed_costs[cow.feed_type] += feed_prices[cow.feed_type] 
                # From the cows feed type get the cost and add it to the feed costs for each feed type.
        total_cost = sum(feed_costs.values())
        # Sum all of the feed costs for each feed type and return the float summed value.
        return total_cost



# Unit Tests
def test_cow():
    cow = Cow('Angus', 'corn', 10, 5)
    assert cow.breed == 'Angus'
    assert cow.feed_type == 'corn'
    assert cow.milk_yield == 10
    assert cow.greenhouse_gas == 5

def test_pen():
    pen = Pen('A', 1)
    assert pen.pen_id == 'A'
    assert pen.max_cows == 1
    assert len(pen.cows) == 0
    cow = Cow('Angus', 'corn', 10, 5)
    assert pen.add_cow(cow) == True
    assert len(pen.cows) == 1
    assert pen.add_cow(cow) == False
    assert len(pen.cows) == 1
    assert pen.remove_cow(cow) == True
    assert len(pen.cows) == 0
    assert pen.remove_cow(cow) == False

def test_farm():
    pen1 = Pen('A', 5)
    pen2 = Pen('B', 5)
    farm = Farm([pen1, pen2])
    cow1 = Cow('Angus', 'corn', 10, 5)
    cow2 = Cow('Jersey', 'hay', 5, 2)
    cows = [cow1, cow2]

    # Test pen allocation
    farm.allocate_cows(cows)
    assert pen1.breed == 'Angus'
    assert pen2.breed == 'Jersey'

    # Test milk yield calculation
    expected_milk_yield = {'A': [10], 'B': [5]}
    assert farm.calculate_milk_yield() == expected_milk_yield

    # Test greenhouse gas emissions
    expected_ghg = 7  # (1 cow of Angus breed * 5 kg CO2 per cow per day) + (1 cows of Jersey breed * 2 kg CO2 per cow per day)
    assert farm.greenhouse_gas_emissions() == expected_ghg

    # Test cost estimation
    expected_cost = 17.5  # (1 cows of Angus breed * 10 kg of corn * $1/kg) + (1 cows of Jersey breed * 5 kg of hay * $1.5/kg)
    feed_prices = {'corn': 10, 'hay': 7.5}
    assert farm.estimate_cost(feed_prices) == expected_cost

test_cow()
test_pen()
test_farm()



# Driver Code 
if __name__ == '__main__':
    # Create some cows
    cow1 = Cow('Holstein', 'grain', 25, 10)
    cow2 = Cow('Jersey', 'grass', 18, 8)
    cow3 = Cow('Ayrshire', 'silage', 20, 9)
    cow4 = Cow('Guernsey', 'grain', 22, 11)

    # Create some pens
    pen1 = Pen('P1', 2)
    pen2 = Pen('P2', 3)
    pen3 = Pen('P3', 2)
    pen4 = Pen('P4', 1)

    # Allocate cows to pens
    farm = Farm([pen1, pen2, pen3, pen4])
    cows = [cow1, cow2, cow3, cow4]
    if farm.allocate_cows(cows):
        print('All cows allocated successfully!')
    else:
        print('Unable to allocate all cows.')

    # Calculate milk yield
    milk_yield_data = farm.calculate_milk_yield()
    for pen_id, milk_yields in milk_yield_data.items():
        print(f'Pen {pen_id} milk yield: {sum(milk_yields)}')

    # Calculate greenhouse gas emissions
    greenhouse_gas = farm.greenhouse_gas_emissions()
    print(f'Total greenhouse gas emissions: {greenhouse_gas}')

    # Estimate feed cost
    feed_prices = {'grain': 5, 'grass': 3, 'silage': 4}
    total_cost = farm.estimate_cost(feed_prices)
    print(f'Total feed cost: {total_cost}')
