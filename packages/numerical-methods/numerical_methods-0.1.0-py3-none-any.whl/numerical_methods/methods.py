def rectangle_method(f, a, b, n):
    """
    Rectangle method for numerically calculaing definite integrals
    Parameters:
    ---------
    f : subintegral function
    
    a : lower limit of integration
    
    b : upper limit of integration
    
    n : int, number of subintervals
    
    Returns
    -------
    solution : list of shape 3, it contains
        solution[0] : approximate integral
        solution[1] : solution approximation process
        solution[2] : boundaries of integration
        
    Example usage:
    ```
    def func(x):
        return 2*x**2 - 3
    a = -1  # lower limit
    b = 4  # upper limit
    n = 100  # number of subintervals
    integral = rectangle_method(func, a, b, n)
    print("Approximate integral:", integral[0]) 
    ```
    >>> Approximate integral: 28.331249999999958
    """
    dx = (b - a) / n
    x = a + dx / 2
    integral = 0
    
    ints, xs = [], []
    for i in range(n):
        f_x = f(x)  # replace function with your own function
        integral += f_x * dx
        x += dx
        ints.append(integral)
        xs.append(x)
    return [integral, ints, xs]

def bisection(function, a, b, e, **kwargs):
    """
    Bisection method for numerically solving unlinear equtaions
    
    Parameters
    ----------
    function : some function what you need to solve at line segment [a, b]
        e.g. 
        ```
        def function(x):
            return x**3 + x - 1
        ```
    
    a and b : let it be numbers satisfying a < b and f(a)*f(b) < 0
    
    e : the desired bound for the error
    
    trace : whether trace progress of algorithm, default: trace = False
    
    Returns
    -------
    m : float - solution of given equation
    ----------
    Algorithm :
    Repeat following steps until h < e (actual errors < desired bound for the error)
    Step 1. Calculate m = (a+b)/2
    Step 2. Calculate f(m) and if f(m) = 0 then stop -> break
    Step 3. Calculate h = |(b-a)/2| for error testing
    Step 4. If f(a)*f(m) < 0 then b = m and if f(a)*f(m) > 0 then a = m
    ---------
    Example usage:
    ```
    def func(x):
            return x**3 + x - 1
    bisection(func, 0, 1, 0.00001)
    ```
    >>> 0.6823348999023438
    """
    h = abs((b-a)/2)
    while h > e:
        m = (a + b)/2
        f_m = function(m)
        if f_m == 0:
            print('f(m)=0, stoping...')
            break
        h = abs((b-a)/2)
        if function(a)*function(m) < 0:
            b = m
        elif function(a)*function(m) > 0:
            a = m
        if kwargs:
            if list(kwargs.values())[0] == True:
                if h > e:
                    print(f"m = {m:.7f}, [a, b] = [{a:.7f}, {b:.7f}], h = {h:.7f} > {e:.7f} = e")
                elif h < e:
                    print(f"x = {m}, [a, b] = [{a}, {b}], h = {h} < {e} = e")
    else:
        if kwargs:
            if list(kwargs.values())[0] == True:
                print('\nactual errors < desired bound for the error -->> solution found: x =')
    return m
