import math

# split a string into mathematical tokens
# returns a list of numbers, operators, parantheses and commas
# output will not contain spaces
def tokenize(string):
    splitchars = list("+-*/(),")
    
    # surround any splitchar by spaces
    tokenstring = []
    for c in string:
        if c in splitchars:
            tokenstring.append(' %s ' % c)
        else:
            tokenstring.append(c)
    tokenstring = ''.join(tokenstring)
    #split on spaces - this gives us our tokens
    tokens = tokenstring.split()
    
    #special casing for **:
    #ADDED: special casting for '-' as a negative ###(TODO: how to evaluate -Constant and -Var etc)###
    ans = []
    for t in tokens:
        if len(ans) > 0 and t == ans[-1] == '*':
            ans[-1] = '**'
        elif len(ans)==1 and ans[0]=='-':
            ans[0]='-'+t
        elif len(ans)>1 and ans[-1]=='-' and ans[-2] in ['+','-','/','*','**','(']:
            ans[-1]='-'+t
        else:
            ans.append(t)
    return ans
   
# check if a string represents a numeric value
def isnumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

# check if a string represents an integer value        
def isint(string):
    try:
        int(string)
        return True
    except ValueError:
        return False



class Expression():
    """A mathematical expression, represented as an expression tree"""
    
    """
    Any concrete subclass of Expression should have these methods:
     - __str__(): return a string representation of the Expression.
     - __eq__(other): tree-equality, check if other represents the same expression tree.
    """
    # TODO: when adding new methods that should be supported by all subclasses, add them to this list
    
    # operator overloading:
    # this allows us to perform 'arithmetic' with expressions, and obtain another expression
    def __add__(self, other):
        print('Expression \t __add__'+str(self)+', '+str(other))
        return AddNode(self, other)
        
    def __sub__(self, other):
        print('Expression \t __sub__'+str(self)+', '+str(other))
        return SubNode(self, other)
        
    def __mul__(self, other):
        print('Expression \t __mul__'+str(self)+', '+str(other))
        return MulNode(self, other)
        
    def __truediv__(self, other):
        print('Expression \t __truediv__'+str(self)+', '+str(other))
        return DivNode(self, other)
        
    def __pow__(self, other):
        print('Expression \t __pow__'+str(self)+', '+str(other))
        return PowNode(self, other)
    
    def __neg__(self):
        print('Expression \t __neg__'+str(self)+', '+str(other))
        return NegNode(self)
        
    # TODO: other overloads, such as __sub__, __mul__, etc.
    def evaluate(self,dictionary=None):
        # the second object represents the dictionary which we will give by ourself (looks for example like {'x':2, 'y':3})
        # the eval class in python uses this automatically (definition)
        if dictionary==None:
            answer = eval(str(self))
            return answer
        else:
            answer=eval(str(self),dictionary)
            return answer
        
    # basic Shunting-yard algorithm
            
    def fromString(string):
        # split into tokens
        tokens = tokenize(string)
        
        # stack used by the Shunting-Yard algorithm
        stack = []
        # output of the algorithm: a list representing the formula in RPN
        # this will contain Constant's and '+'s
        output = []
        
        # list of operators incl their operator value
        oplist = {'+':2,'-':2,'/':3,'*':3,'**':4}
        
        for token in tokens:
            if isnumber(token):
                # numbers go directly to the output
                if isint(token):
                    output.append(Constant(int(token)))
                else:
                    output.append(Constant(float(token)))
                    
            elif token in oplist:
                # pop operators from the stack to the output until the top is no longer an operator
                while True:
                    # TODO: when there are more operators, the rules are more complicated
                    # look up the shunting yard-algorithm
                    # ADDED: also stop output.append(stack.pop() when operator value of stack[-1] is smaller then operator value of token, or when token=='**' (because of right associativity)
                    if len(stack) == 0 or stack[-1] not in oplist or oplist[token] == 4 or oplist[token] > oplist[stack[-1]]:
                        break
                    output.append(stack.pop())
                # push the new operator onto the stack
                stack.append(token)
            elif token == '(':
                # left parantheses go to the stack
                    stack.append(token)
            elif token == ')':
                # right paranthesis: pop everything upto the last left paranthesis to the output
                while not stack[-1] == '(':
                    output.append(stack.pop())
                # pop the left paranthesis from the stack (but not to the output)
                stack.pop()
            # TODO: do we need more kinds of tokens?
            #ADDED: if token is a small alphabetic letter --> make it an Variable and send it to output
            ####TODO: Do we want to leave some letters (a-e?) to auto make them Constants?
            elif ord(token)>=97 and ord(token)<=122:
                output.append(Variable(str(token)))
            else:
                # unknown token
                raise ValueError('Unknown token: %s' % token)
     
        # pop any tokens still on the stack to the output
        while len(stack) > 0:
            output.append(stack.pop())

        # convert RPN to an actual expression tree
        oplist = list(oplist)
        for t in output:
            if t in oplist:
                # let eval and operator overloading take care of figuring out what to do
                y = stack.pop()
                x = stack.pop()
                stack.append(eval('x %s y' % t))
            else:
                # a constant, push it to the stack
                stack.append(t)
        # the resulting expression tree is what's left on the stack
        return stack[0]

class Constant(Expression):
    """Represents a constant value"""
    def __init__(self, value, precedence = 6):
        self.value = value
        print('Constant(Expression) \t __init__'+str(self.value))
        if self.value < 0 : 
            self.precedence = 3
        else: 
            self.precedence = 6
            
    def __eq__(self, other):
        if isinstance(other, Constant):
            return self.value == other.value
        else:
            return False
        
    def __str__(self):
        print('Constant(Expression) \t __str__'+str(self.value))
        return str(self.value)
        
    # allow conversion to numerical values
    def __int__(self):
        return int(self.value)
        
    def __float__(self):
        return float(self.value)
    
    
        
class Variable(Expression):
    """Represents a variable value"""
    def __init__(self, value, precedence=6):
        self.value = value
        self.precedence=precedence
        print('Variable(Expression) \t __init__'+str(self.value))
        
    def __str__(self):
        print('Variable(Expression) \t __str__'+str(self.value))
        return str(self.value)
    
    def __eq__(self,other):
        if isinstance(other,Variable):
            return self.value==other.value
        else:
            return False
        
    
        
        
class BinaryNode(Expression):
    """A node in the expression tree representing a binary operator."""

    def __init__(self, lhs, rhs, op_symbol, precedence=0, associativity=0):
        print('BinaryNode(Expression) \t __init__')
        self.lhs = lhs
        self.rhs = rhs
        self.op_symbol = op_symbol
        self.precedence = precedence
        self.associativity = associativity
    #ADDED: list of operators incl their operator value

    # TODO: what other properties could you need? Precedence, associativity, identity, etc.
            
    def __eq__(self, other):
        if type(self) == type(other):
            return self.lhs == other.lhs and self.rhs == other.rhs
        else:
            return False
            
    def __str__(self):
        print('BinaryNode(Expression) \t __str__')
        lstring = str(self.lhs)
        rstring = str(self.rhs)
        
        # ADDED: check whether the type of the lhs node is a BinaryNode and if parenthesis are necessary for AT LEAST the lhs node

        if self.precedence > self.lhs.precedence:

            # ADDED: check whether the type of the rhs node is a BinaryNode and if parenthesis are needed around rhs node, by checking if one of the following is true:
            #the operator value of current BinaryNode is greater than the operator value of the rhs node, or 
            #the value of the current BinaryNode AND of the rhs node are equal to '**', (ergo power operation value of 4 and right associative) 
            # Notice: we check the last condition only for the rhs, because the power operator is right associative.
            if self.precedence > self.rhs.precedence or (self.precedence == self.rhs.precedence and self.associativity == 'left'):
                print("(%s) %s (%s)" % (lstring, self.op_symbol, rstring))
                return "(%s) %s (%s)" % (lstring, self.op_symbol, rstring)
            # ADDED: if not, add only parenthesis to the lhs    
            else:
                print("(%s) %s %s" % (lstring, self.op_symbol, rstring))
                return "(%s) %s %s" % (lstring, self.op_symbol, rstring)
    
        # ADDED: if not, check whether the type of the rhs node is a BinaryNode and if parenthesis are necessary for the rhs node (checking procedure equal to the above one)

        elif self.precedence > self.rhs.precedence or (self.precedence == self.rhs.precedence and self.associativity == 'left'):
            print("%s %s %s" % (lstring, self.op_symbol, rstring))
            return "%s %s (%s)" % (lstring, self.op_symbol, rstring)
        
                
        #ADDED: Simplify trivial expressions, e.g 'x+0'='x' for example
        if isinstance(self, MulNode):
            # 'x*0'='0' and '0*x'='0'
            if self.lhs==Constant(0) or self.rhs==Constant(0):
                return str(Constant(0))
            # 'x*1'='x'
            elif self.rhs==Constant(1):
                return lstring
            # '1*x'='x'
            elif self.lhs == Constant(1):
                return rstring
            ### x*b=b*x, x anything
            #TODO: also with DivNode?
            elif isinstance(self.rhs,Constant) and not isinstance(self.lhs,Constant):
                return str(self.rhs*self.lhs)
            # 'x*x'='x**2'
            elif self.lhs==self.rhs:
                ########### HIER MOET DE NODE AANGEPAST WORDEN IPV ANDERS GEPRINT###################
                return str(self.lhs**Constant(2))
            # x**b*x=x**(b+1) and x**b*x**a=x**(b+a) 
            elif isinstance(self.lhs,PowNode):
                if isinstance(self.rhs,PowNode) and self.lhs.lhs==self.rhs.lhs:
                    return str(self.lhs.lhs**(self.lhs.rhs+self.rhs.rhs))
                elif self.lhs.lhs==self.rhs:
                    return str(self.rhs**(self.lhs.rhs+Constant(1)))
                else:
                    a = "%s %s %s" % (self.lhs, self.op_symbol, self.rhs)
                    return a
            #x*x**b=x**(1+b)
            elif isinstance(self.rhs,PowNode):
                if self.lhs==self.rhs.lhs:
                    return str(self.lhs**(Constant(1)+self.rhs.rhs))
                else:
                    a = "%s %s %s" % (self.lhs, self.op_symbol, self.rhs)
                    return a    
            else:
                a = "%s %s %s" % (self.lhs, self.op_symbol, self.rhs)
                return a

        elif isinstance(self.lhs, PowNode):
            a = "%s %s %s" % (lstring, self.op_symbol, rstring)
            return a
            #return partial_evaluation(a)

        elif isinstance(self, AddNode):
            #'0+x'='x'
            if self.lhs==Constant(0):
                return rstring
            #'x+0'='x'
            elif self.rhs==Constant(0):
                return lstring
            else:
                print('BinaryNode(Expression) \t __str__ \t isinstance AddNode \t else')
                print("%s %s %s" % (lstring, self.op_symbol, rstring))
                a = "%s %s %s" % (lstring, self.op_symbol, rstring)
                return a
                #return partial_evaluation(a)
                
        elif isinstance(self, DivNode):
            # 'x/1'='x'
            if self.rhs==Constant(1):
                return lstring
            else:
                a = "%s %s %s" % (lstring, self.op_symbol, rstring)
                return a
                #return partial_evaluation(a)
                
        
        # ADDED: if everything doesn't hold, then return the general case without parenthesis. 
        else:
            print("%s %s %s" % (lstring, self.op_symbol, rstring))
            a = "%s %s %s" % (lstring, self.op_symbol, rstring)
            return a
            #return partial_evaluation(a)


        
class UnaryNode(Expression):
    """A node in the expression tree representing a unary operator."""
    def __init__(self, operand, op_symbol=None, precedence=0):
        self.operand = operand
        self.op_symbol = op_symbol
        self.precedence = precedence
        print(self.precedence)
    
    def __str__(self):
        return self.op_symbol+str(self.operand)

#class Derivative(BinaryNode): 
    
class AddNode(BinaryNode):
    """Represents the addition operator"""
    def __init__(self, lhs, rhs):
        print('AddNode(BinaryNode) \t __init__')
        super(AddNode, self).__init__(lhs, rhs, '+', 1, 'both')

class SubNode(BinaryNode):
    """Represents the substraction operator"""
    def __init__(self, lhs, rhs):
        print('SubNode(BinaryNode) \t __init__')
        super(SubNode, self).__init__(lhs, rhs, '-', 1, 'left')
        
class MulNode(BinaryNode):
    """Represents the multiplication operator"""
    def __init__(self, lhs, rhs):
        print('MulNode(BinaryNode) \t __init__')
        super(MulNode, self).__init__(lhs, rhs, '*', 2, 'both')
        
class DivNode(BinaryNode):
    print('DivNode(BinaryNode) \t __init__')
    """Represents the division operator"""
    def __init__(self, lhs, rhs):
        super(DivNode, self).__init__(lhs, rhs, '/', 2, 'left')

class PowNode(BinaryNode):
    print('PowNode(BinaryNode) \t __init__')
    """Represents the power operator"""
    def __init__(self, lhs, rhs):
        super(PowNode, self).__init__(lhs, rhs, '**', 4, 'right')

class NegNode(UnaryNode):
    print('NegNode(UnaryNode) \t __init__')
    """Represents the negation operator"""
    def __init__(self, operand):
        super(NegNode, self).__init__(operand, '-', 3)



# TODO: add more subclasses of Expression to represent operators, variables, functions, etc.

# ADDED: evaluate a part of the string
def deler(x,y):
    antwoord=y%x
    return antwoord

def ggd(x,y):
    if y<x:
        return ggd(y,x)
    elif x == y:
        return x
    elif x == 0 and y == 0:
        return 0
    elif x == 0:
        return y
    elif y == 0:
        return x
    else:
        return ggd(x,deler(x,y))

def partial_evaluation(a):
    # ADDED: try whether there is something in the string that could be evaluated
    try:
        b = eval(a)
        if isinstance(b,float):
            return a
        else:
            return str(b)
    # ADDED: if not, then return a if there is a TypeError
    except TypeError: 
        return a
    # ADDED: if not, then return a if there is a NameError
    except NameError: 
        return a

def deriv(y,x):
    if y==x:
        return Constant(1)
    else:
        return Constant(0)