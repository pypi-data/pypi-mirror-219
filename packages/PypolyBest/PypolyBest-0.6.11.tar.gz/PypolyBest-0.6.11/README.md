##DOCUMENTATION

PypolyBest has a class named polyBest. 
Constructor of this class accepts four parameters:
    1. Feature Data-frame(a matrix type object)
    2. Target Data-frame(a matrix type object)
    3*. A list of coefficients of regularization for lasso regression of degree 1,2,3,.. 
       in that order upto whatver degree you would like to do polynomial regression.
    4. Train-Test split ratio
    5. boolean value, pass True if u want to do StandardScaler else pass False
The class has two methods:
    1. mseScore(): takes no parameters, returns a list of mse scores of len(3*).
    2. maescore(): takes no parameters, returns a list of mae scores of len(3*)