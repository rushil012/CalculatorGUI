# author: Rushil Nagpal
# date: May 11, 2023
# file: tree.py , has the class BinaryTree() and a subclass ExpTree(BinaryTree)
# input:  object such as t= ExpTree(BinaryTree)
# output: the object which is a binary tree and using transversal methods to calculate expressions

from stack import Stack                     #using Stack class

class BinaryTree:
    def __init__(self,rootObj=None):
        self.key = rootObj
        self.leftChild = None
        self.rightChild = None
    def insertLeft(self,newNode):
        if self.leftChild == None:
            self.leftChild = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.leftChild = self.leftChild
            self.leftChild = t
    def insertRight(self,newNode):
        if self.rightChild == None:
            self.rightChild = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.rightChild = self.rightChild
            self.rightChild = t
    def getRightChild(self):
        return self.rightChild
    def getLeftChild(self):
        return self.leftChild
    def setRootVal(self,obj):
        self.key = obj
    def getRootVal(self):
        return self.key
    def __str__(self):
        s = f"{self.key}"
        s += '('
        if self.leftChild != None:
            s += str(self.leftChild)
        s += ')('
        if self.rightChild != None:
            s += str(self.rightChild)
        s += ')'
        return s
def is_float(string):           #checking if it is a float
    try:
        float(string)
        return True
    except ValueError:
        return False
class ExpTree(BinaryTree):
    def make_tree(postfix):
        rt = Stack()
        sett = set(['+', '-', '*', '/', '^'])               #set of operators
        for x in postfix:       
            if x.isalnum() or is_float(x):                  #checking if x is a operator
                rt.push(ExpTree(x))
            elif x in sett:
                temp = ExpTree(x)
                temp.rightChild = rt.pop()                      #making the tree from postfix
                temp.leftChild = rt.pop()                         
                rt.push(temp)
        return rt.pop()
    def preorder(tree):
        s = ''                                              #preorder transversal method
        if tree != None:
            s = tree.getRootVal()
            s += ExpTree.preorder(tree.getLeftChild())
            s += ExpTree.preorder(tree.getRightChild())
        return s
    def inorder(tree):
        if tree == None:                                    #inorder transversal method
            return ""
        if tree != None:
            ss = ExpTree.inorder(tree.getLeftChild())
            tt = tree.getRootVal()
            yy = ExpTree.inorder(tree.getRightChild())
        if ss and yy:
            return f"({ss}{tt}{yy})"
        elif tt:
            return f"{ss}{tt}"
        elif yy:
            return f"{tt}({yy})"
        else:
            return tt
    def postorder(tree):
        s = ''                                               #postorder transversal method
        if tree != None:
            s = ExpTree.postorder(tree.getLeftChild())
            s += ExpTree.postorder(tree.getRightChild())
            s += tree.getRootVal()
        return s
    def evaluate(tree):
        if tree == None:
            return None
        if tree.getLeftChild() == None and tree.getRightChild() == None:
            return float(tree.getRootVal())
        l_val = ExpTree.evaluate(tree.getLeftChild())
        r_val = ExpTree.evaluate(tree.getRightChild())

        if tree.getRootVal() == "+":                                        #writing code according to the operators
            return l_val + r_val
        elif tree.getRootVal() == "-":
            return l_val - r_val
        elif tree.getRootVal() == "*":
            return l_val * r_val
        elif tree.getRootVal() == "/":
            if r_val == 0:
                print("Division by zero not possible")
                return ""
            else:
                return l_val / r_val
        elif tree.getRootVal() == "^":
            return l_val ** r_val
        return 0
            
    def __str__(self):
        return ExpTree.inorder(self)                            #the str of inorder is same as infix
# a driver for testing BinaryTree and ExpTree
if __name__ == '__main__':
    # test a BinaryTree
    r = BinaryTree('a')
    assert r.getRootVal() == 'a'
    assert r.getLeftChild()== None
    assert r.getRightChild()== None
    assert str(r) == 'a()()'
    r.insertLeft('b')
    assert r.getLeftChild().getRootVal() == 'b'
    assert str(r) == 'a(b()())()'
    r.insertRight('c')
    assert r.getRightChild().getRootVal() == 'c'
    assert str(r) == 'a(b()())(c()())'
    r.getLeftChild().insertLeft('d')
    r.getLeftChild().insertRight('e')
    r.getRightChild().insertLeft('f')
    assert str(r) == 'a(b(d()())(e()()))(c(f()())())'
    assert str(r.getRightChild()) == 'c(f()())()'
    assert r.getRightChild().getLeftChild().getRootVal() == 'f'
    # test an ExpTree
    postfix = '5 2 3 * +'.split()
    tree = ExpTree.make_tree(postfix)
    assert str(tree) == '(5+(2*3))'
    assert ExpTree.inorder(tree) == '(5+(2*3))'
    assert ExpTree.postorder(tree) == '523*+'
    assert ExpTree.preorder(tree) == '+5*23'
    assert ExpTree.evaluate(tree) == 11.0
    postfix = '5 2 + 3 *'.split()
    tree = ExpTree.make_tree(postfix)
    assert str(tree) == '((5+2)*3)'
    assert ExpTree.inorder(tree) == '((5+2)*3)'
    assert ExpTree.postorder(tree) == '52+3*'
    assert ExpTree.preorder(tree) == '*+523'
    assert ExpTree.evaluate(tree) == 21.0
