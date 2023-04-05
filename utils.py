
def choose(obj,values):
    """
    Ask user to choose between a list of elements.

    Parameters
    ----------
    obj : str
        type of the elements
    values : [str]
        list of possible choices

    Return
    ------
    chosen : str
        chosen value

    Example
    -------
    choice = choose("animal",["dog","cat","horse"])

    Choose animal ...
    1 : dog
    2 : cat
    3 : horse
    animal = 
    
    """

    n = len(values)
    allowed_choices = [str(i) for i in range(1,n+1)]
    msg = "Choose {} ...\n".format(obj)
    msg += "\n".join([str(i+1) + " : " + str(values[i]) for i in range(n)])
    while True:
        print(msg)
        choice = input("{} = ".format(obj))
        if choice in allowed_choices:
            break
        print("Incorrect choice. Try again ...\n")
    chosen = values[int(choice)-1]
    return chosen
    
    