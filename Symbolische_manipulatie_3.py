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
    
    #### goed onderscheid maken: wat willen wij NIET zien --> in binaryNode extra if deel, wat willen wij WEL zien HIERONDER
    #### in binary stijl, dus 5*x=5x hoor bij wat we NIET willen zien
    
    def __add__(self, other):
        return AddNode(self, other)
        
    def __sub__(self, other):
        # 'x-x=0*x'
        # 'a*x-b*x=(a-b)*x'
        # 'a*x-x=(a-1)*x'
        # 'x-a*x=(1-a)*x'
        return SubNode(self, other)
        
    def __mul__(self, other):
        # We want a Constant in front of a non Constant
        # 'x*x=x**2'
        # 'a*x*x=a*x**2' # drietallen moeten apart omdat eerste tweetal andere combi
        # 'x**a*x**b=x**(a+b)
        # 'c*x**a*x**b=c*x**(a+b)' ##### WERKT NIET
        # 'x**a*x=x**(a+1)'
        # 'x*x**a=x**(1+a)'
        return MulNode(self, other)
        
    def __truediv__(self, other):
        # 'a*x/b=a/b*x'
        # 'x/x=x**0'
        # 'x**a/x**b=x**(a-b)
        # 'x**a/x=x**(a-1)'
        # 'x/x**a=x**(1-a)'
        return DivNode(self, other)
        
    def __pow__(self, other):
        return PowNode(self, other)
    
    def __neg__(self):
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
        return str(self.value)
        
    # allow conversion to numerical values
    def __int__(self):
        return int(self.value)
        
    def __float__(self):
        return float(self.value)
        
    def simplify(self):
        return self
    
        
class Variable(Expression):
    """Represents a variable value"""
    def __init__(self, value, precedence=6):
        self.value = value
        self.precedence=precedence
        
    def __str__(self):
        return str(self.value)
    
    def __eq__(self,other):
        if isinstance(other,Variable):
            return self.value==other.value
        else:
            return False
    
    def simplify(self):
        return self
        
    
        
        
class BinaryNode(Expression):
    """A node in the expression tree representing a binary operator."""

    def __init__(self, lhs, rhs, op_symbol, precedence=0, associativity=0):
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
        lstring = str(self.lhs)
        rstring = str(self.rhs)
        
        # ADDED: check whether the type of the lhs node is a BinaryNode and if parenthesis are necessary for AT LEAST the lhs node

        if self.precedence > self.lhs.precedence:

            # ADDED: check whether the type of the rhs node is a BinaryNode and if parenthesis are needed around rhs node, by checking if one of the following is true:
            #the operator value of current BinaryNode is greater than the operator value of the rhs node, or 
            #the value of the current BinaryNode AND of the rhs node are equal to '**', (ergo power operation value of 4 and right associative) 
            # Notice: we check the last condition only for the rhs, because the power operator is right associative.
            if self.precedence > self.rhs.precedence or (self.precedence == self.rhs.precedence and self.associativity == 'left'):
                return "(%s) %s (%s)" % (lstring, self.op_symbol, rstring)
            # ADDED: if not, add only parenthesis to the lhs    
            else:
                return "(%s) %s %s" % (lstring, self.op_symbol, rstring)
    
        # ADDED: if not, check whether the type of the rhs node is a BinaryNode and if parenthesis are necessary for the rhs node (checking procedure equal to the above one)

        elif self.precedence > self.rhs.precedence or (self.precedence == self.rhs.precedence and self.associativity == 'left'):
            return "%s %s (%s)" % (lstring, self.op_symbol, rstring)
                
        
        # ADDED: if everything doesn't hold, then return the general case without parenthesis. 
        else:
            a = "%s %s %s" % (lstring, self.op_symbol, rstring)
            return a
            #return partial_evaluation(a)

        
class UnaryNode(Expression):
    """A node in the expression tree representing a unary operator."""
    def __init__(self, operand, op_symbol=None, precedence=0):
        self.operand = operand
        self.op_symbol = op_symbol
        self.precedence = precedence
    
    def __str__(self):
        return self.op_symbol+str(self.operand)

#class Derivative(BinaryNode): 

class AddNode(BinaryNode):
    """Represents the addition operator"""
    def __init__(self, lhs, rhs):
        super(AddNode, self).__init__(lhs, rhs, '+', 1, 'both')

    def simplify(self):
        left=self.lhs
        right=self.rhs
        L=left.simplify()
        R=right.simplify()
        print(str(self)+' add')
        print(type(left))
        print(left)
        print(right)
        # Simplify when childs are Constants
        if type(left)==type(right)==Constant:
            a=left.value+right.value
            return Constant(a)
        # Constants should be right of a non Constant
        elif type(left)==Constant and type(right)!=Constant:
            return (right+left).simplify()
        #(x+a)+b
        elif type(left)==AddNode and type(left.rhs)==type(right)==Constant:
            a=left.rhs.value+right.value
            return (left.lhs+Constant(a)).simplify()
        # x+0=x
        elif right==Constant(0):
            return left.simplify()
        # x+x=2*x
        elif left==right:
            return (Constant(2)*right)
        # a*x+b*x=(a+b)*x
        elif type(left)==type(right)==MulNode and left.rhs==right.rhs:
            return ((left.lhs+right.lhs)*left.rhs).simplify()
        # a*x+x=(a+1)*x
        elif type(left)==MulNode and left.rhs==right:
            return ((left.lhs+Constant(1))*left.rhs).simplify()
        # x+a*x=(1+a)*x
        elif type(right)==MulNode and left==right.rhs:
            return ((Constant(1)+right.lhs)*left).simplify()


        # if left can be simplified, simplify at least left
        elif not L==left:
            #if also right can be simplified, also simplify right
            if not R==right:
                print('left and right can be simplified to '+str(L)+' and '+str(R))
                return (L+R).simplify()
            #only left can be simplified
            else:
                print('only left can be simplified to '+str(L))
                return (L+right).simplify()

        #if only right can be simplified, simplify only right
        elif not R==right:
            print('only right can be simplified to '+str(R))
            return (left+R).simplify()
        else:
            print('nothing can be simplified')
            return left+right

class SubNode(BinaryNode):
    """Represents the substraction operator"""
    def __init__(self, lhs, rhs):
        super(SubNode, self).__init__(lhs, rhs, '-', 1, 'left')

    def simplify(self):
        left=self.lhs
        right=self.rhs
        L=left.simplify()
        R=right.simplify()
        print(str(self)+' sub')
        print(type(left))
        print(left)
        print(right)
        # Simplify when childs are Constants
        if type(left)==type(right)==Constant:
            a=left.value-right.value
            return Constant(a)
        # Constants should be right of a non Constant
        #elif type(left)==Constant and type(right)!=Constant:
        #    return (right+left).simplify()
        #(x-a)-b=x-(a+b)
        elif type(left)==SubNode and type(left.rhs)==type(right)==Constant:
            a=left.rhs.value+right.value
            return (left.lhs-Constant(a)).simplify()
        # x-0=x
        elif right==Constant(0):
            return left.simplify()
        # x-x=0
        elif left==right:
            return Constant(0)
        # a*x-b*x=(a-b)*x
        elif type(left)==type(right)==MulNode and left.rhs==right.rhs:
            return ((left.lhs-right.lhs)*left.rhs).simplify()
        # a*x+x=(a-1)*x
        elif type(left)==MulNode and left.rhs==right:
            return ((left.lhs-Constant(1))*left.rhs).simplify()
        # x-a*x=(1-a)*x
        elif type(right)==MulNode and left==right.rhs:
            return ((Constant(1)-right.lhs)*left).simplify()
        # if left can be simplified, simplify at least left
        elif not L==left:
            #if also right can be simplified, also simplify right
            if not R==right:
                print('left and right can be simplified to '+str(L)+' and '+str(R))
                return (L-R).simplify()
            #only left can be simplified
            else:
                print('only left can be simplified to '+str(L))
                return (L-right).simplify()

        #if only right can be simplified, simplify only right
        elif not R==right:
            print('only right can be simplified to '+str(R))
            return (left-R).simplify()
        else:
            print('nothing can be simplified')
            return left-right

class MulNode(BinaryNode):
    """Represents the multiplication operator"""
    def __init__(self, lhs, rhs):
        super(MulNode, self).__init__(lhs, rhs, '*', 2, 'both')

    def simplify(self):
        left=self.lhs
        right=self.rhs
        L=left.simplify()
        R=right.simplify()
        print(str(self)+' mul')
        print(type(left))
        print(left)
        print(right)
        # Simplify when childs are Constants
        if type(left)==type(right)==Constant:
            a=left.value*right.value
            return Constant(a)
        # x*a=a*x
        elif type(right)==Constant and type(left)!=Constant:
            return (right*left).simplify()
        #a*(b*x)=(a*b)*x
        elif type(right)==MulNode and type(left)==type(right.lhs)==Constant:
            a=left.value*right.lhs.value
            return (Constant(a)*right.rhs).simplify()
        # 1*x=x
        elif left==Constant(1):
            return right.simplify()
        # 0*x=0
        elif left==Constant(0):
            return Constant(0)
        # x*x=x**2
        elif left==right:
            return (left**Constant(2)).simplify()
        # x**a*x**b=x**(a+b)
        elif type(left)==type(right)==PowNode and left.lhs==right.lhs:
            return (left.lhs**(left.rhs+right.rhs)).simplify()
        # x**a*x=x**(a+1)
        elif type(left)==PowNode and left.lhs==right:
            return (left.lhs**(left.rhs+Constant(1))).simplify()
        # x*x**a=x**(1+a)
        elif type(right)==PowNode and left==right.lhs:
            return (left**(Constant(1)+right.rhs)).simplify()


        # if left can be simplified, simplify at least left
        elif not L==left:
            #if also right can be simplified, also simplify right
            if not R==right:
                print('left and right can be simplified to '+str(L)+' and '+str(R))
                return (L*R).simplify()
            #only left can be simplified
            else:
                print('only left can be simplified to '+str(L))
                return (L*right).simplify()

        #if only right can be simplified, simplify only right
        elif not R==right:
            print('only right can be simplified to '+str(R))
            return (left*R).simplify()
        else:
            print('nothing can be simplified')
            return left*right

        #def derivative(self,other):
        #    iets=self.simplify()
        #   if type(iets.lhs)!= BinaryNode and :
        #        return 

        
class DivNode(BinaryNode):
    """Represents the division operator"""
    def __init__(self, lhs, rhs):
        super(DivNode, self).__init__(lhs, rhs, '/', 2, 'left')

    def simplify(self):
        left=self.lhs
        right=self.rhs
        L=left.simplify()
        R=right.simplify()
        print(str(self)+' div')
        print(type(left))
        print(left)
        print(right)
        # Simplify when childs are Constants
        if type(left)==type(right)==Constant:
            a=left.value/right.value
            return Constant(a)
        # x/1 = x
        elif right==Constant(1):
            return left.simplify()
        # x/a=(1/a)*x
        elif type(right)==Constant:
            return ((Constant(1)/right)*left).simplify()
        # 0/x=0
        elif left==Constant(0):
            return Constant(0)
        # x/x=1
        elif left==right:
            return Constant(1)
        # x**a/x**b=x**(a-b)
        elif type(left)==type(right)==PowNode and left.lhs==right.lhs:
            return (left.lhs**(left.rhs-right.rhs)).simplify()
        # x**a*x=x**(a-1)
        elif type(left)==PowNode and left.lhs==right:
            return (left.lhs**(left.rhs-Constant(1))).simplify()
        # x*x**a=x**(1-a)
        elif type(right)==PowNode and left==right.lhs:
            return (left**(Constant(1)-right.rhs)).simplify()

        # if left can be simplified, simplify at least left
        elif not L==left:
            #if also right can be simplified, also simplify right
            if not R==right:
                print('left and right can be simplified to '+str(L)+' and '+str(R))
                return (L/R).simplify()
            #only left can be simplified
            else:
                print('only left can be simplified to '+str(L))
                return (L/right).simplify()

        #if only right can be simplified, simplify only right
        elif not R==right:
            print('only right can be simplified to '+str(R))
            return (left/R).simplify()
        else:
            print('nothing can be simplified')
            return left/right

class PowNode(BinaryNode):
    """Represents the power operator"""
    def __init__(self, lhs, rhs):
        super(PowNode, self).__init__(lhs, rhs, '**', 4, 'right')

    def simplify(self):
        left=self.lhs
        right=self.rhs
        L=left.simplify()
        R=right.simplify()
        print(str(self)+' pow')
        print(type(left))
        print(left)
        print(right)
        # Simplify when childs are Constants
        if type(left)==type(right)==Constant:
            a=left.value**right.value
            return Constant(a)
        # x**1=x
        elif right==Constant(1):
            return left.simplify()
        # x**0=1
        elif right==Constant(0):
            return Constant(1)
        # (x**a)**b=x**(a*b)
        elif type(left)==PowNode:
            return (left.lhs**(left.rhs*right)).simplify()
        # if left can be simplified, simplify at least left
        elif not L==left:
            #if also right can be simplified, also simplify right
            if not R==right:
                print('left and right can be simplified to '+str(L)+' and '+str(R))
                return (L**R).simplify()
            #only left can be simplified
            else:
                print('only left can be simplified to '+str(L))
                return (L**right).simplify()

        #if only right can be simplified, simplify only right
        elif not R==right:
            print('only right can be simplified to '+str(R))
            return (left**R).simplify()
        else:
            print('nothing can be simplified')
            return left**right

class NegNode(UnaryNode):
    """Represents the negation operator"""
    def __init__(self, operand):
        super(NegNode, self).__init__(operand, '-', 3)

    def simplify(self):
        if type(self.operand)==Constant:
            a= -1*self.operand.value
            return Constant(a)
        else:
            return self



# TODO: add more subclasses of Expression to represent operators, variables, functions, etc.

# ADDED: evaluate a part of the string

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

