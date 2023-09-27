# author: Rushil Nagpal
# date: May 11, 2023
# file: calculator.py , a calculator which calculates the expression
# input: the infix expression
# output: the evaluation of the expression

from stack import Stack
from tree import BinaryTree, ExpTree
import re                                           #regular expression module
def is_float(string):                   #function for checking if the string is a float or not
    try:
        float(string)
        return True
    except ValueError:
        return False
def infix_to_postfix(infix):
    precedence = {"(":1,"-":2,"+":2,"/":3,"*":3,"^":4}          #dictionary for marking the precedence
    opStack = Stack()                                           #taking an empty stack
    postfixList = []                                            #empty list for putting postfix expression
    forms = re.split(r'([-+*/()^])', infix)                     #using re module to split the expression by operators
    # Remove any empty strings from the list
    tokenList = [i for i in forms if i.strip()] 
    for token in tokenList:
        if token.isalnum() or is_float(token):                  #checking for alphanumeric or float value
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)                                 #pushing to stack if it has a starting bracket "("
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':                              #condition for appending the token till ")"
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and (precedence[opStack.peek()] >= precedence[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)
    while not opStack.isEmpty():
        postfixList.append(opStack.pop())                       #postfix in the list
    return " ".join(postfixList)                                #returning the string postfix expression
def calculate(infix):   
    t = infix_to_postfix(infix)                             #converting to postfix
    tr = t.split()                                          #converting to list for parameter for make_tree func
    to = ExpTree.make_tree(tr)                              #making tree
    return ExpTree.evaluate(to)                             #using the value in evaluate func
# a driver to test calculate module
if __name__ == '__main__':
    # test infix_to_postfix function
    assert infix_to_postfix('5+2*3') == '5 2 3 * +'
    # test calculate function
    assert calculate('(5+2)*3') == 21.0
    assert calculate('5+2*3') == 11.0
    print("Welcome to Calculator Program!")
    rt = True
    while rt:
        xy = input("Please enter your expression here. To quit enter 'quit' or 'q':\n")         #loop condition
        if xy == "quit" or xy == "q":
            rt = False
            break
        print(calculate(xy))                                                                    #printing the result
    print("Goodbye!")