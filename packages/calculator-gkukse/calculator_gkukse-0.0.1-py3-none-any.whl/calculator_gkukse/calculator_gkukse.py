NUMBER_BOOUNDARY=1e-6 # number error boundary

""" All functions take in int or float values """
def user_number_validity(user_number):
    assert isinstance(float(user_number), float), f"Value '{user_number}' is not a number"


class Calculator:
    Overall_sum:float=0.0  # The starting sum is alomost 0

    def __init__(self) -> None: pass

    """ Addition function adds the numbers to previous sum """
    def Addition(self, user_number:float):
        user_number_validity(user_number)
        self.Overall_sum += user_number
        return(self.Overall_sum)

    """ Subtraction function substracts the numbers from previous sum """
    def Subtraction(self, user_number:float):
        user_number_validity(user_number)
        self.Overall_sum -= user_number
        return(self.Overall_sum)

    """ Multiplication function multiplies the number with previous sum """
    def Multiplication(self, user_number:float):
        user_number_validity(user_number)
        self.Overall_sum *= user_number
        return(self.Overall_sum)

    """ Division function devides the number out of previous sum, where number is not zero"""
    def Division(self, user_number:float):
        assert (float(abs(user_number))>=NUMBER_BOOUNDARY), f"Value '{user_number}' is not a allowed for devision"
        user_number_validity(user_number)

        self.Overall_sum //= user_number 
        return(self.Overall_sum)

    """ Root function resturns root of sum, by power of number, where number is positive number """    
    def Root(self, root:int):

        assert (abs(root)>NUMBER_BOOUNDARY), f"Value '{root}' is not a allowed for root"
        assert isinstance(int(root), int), f"Value '{root}' is not a number"

        self.Overall_sum = self.Overall_sum**(1/root) # x**(1/n), (n) root of a number
        return(self.Overall_sum)

    """ Resets the sum to 0 """
    def Reset_memory(self):
        self.Overall_sum=0.0
        return(self.Overall_sum)


calculator=Calculator() # writing Calculator() each time is not nice, calculator is more nice


