class treeNode():
    def __init__(self, data=None, left=None, right=None, balance=None, height=0, ancestor=None):
        self.data = data
        self.left = left
        self.right = right
        self.balance = balance
        self.height = height
        self.ancestor = ancestor

    def create_copy(self):
        copy = treeNode(self.data, self.left, self.right, self.balance, self.height, self.ancestor)
        return copy

line = input()
inputs = list(map(int, line.split(',')))


input_operations = []
while True:
	try:
		line = input()
		input_operations.append(line)
	except:
		break

root = treeNode()
root.data = inputs[0]

operations = []


def appendNode(node, num1):
    if num1 < node.data:
        if node.left == None:
            node.left = treeNode()
            node.left.data = num1
            node.left.ancestor = node
        else:
            appendNode(node.left, num1)
    else:
        if node.right == None:
            node.right = treeNode()
            node.right.data = num1
            node.right.ancestor = node
        else:
            appendNode(node.right, num1)



def checkBalanceFindCriticalNode(node, shouldPrint=False):
    left_height = -1
    right_height = -1
    
    if node.left != None:
        left_height = node.left.height
    if node.right != None:
        right_height = node.right.height

    balance = left_height - right_height
    node.balance = balance
    if abs(balance) > 1:
        #print("WARNING WARNING WARNING: OUT OF TRESHOLD OF BALANCE")
        return node
    else:
        return False


def updateHeight(node, sholdPrint = False):
    if node.left != None:
        left_height = node.left.height
    else:
        left_height = -1

    if node.right != None:
        right_height = node.right.height
    else:
        right_height = -1

    node.height = max(left_height, right_height) + 1
    #print(f'    updating: {node.data} to height: {node.height}')

def postOrder(node, shouldPrint = False):
    if node.left != None:
        postOrder(node.left, shouldPrint)
    
    if node.right != None:
        postOrder(node.right, shouldPrint)

    updateHeight(node, shouldPrint)
    whichNode = checkBalanceFindCriticalNode(node, shouldPrint)
    if whichNode != False:
        resultNodes.append(whichNode)
    else:
        return False

def leftRotate(z):
    temp = None
    if z.ancestor != None:
        temp = z.ancestor

    # get the information out of it before replacing it
    y = z.right
    t2 = z.right.left

    y.left = z
    y.left.right = t2

    if y.left != None:
        y.left.ancestor = y
    if y.left.right != None:
        y.left.right.ancestor = y.left

    y.ancestor = temp

    return y

def rightRotate(z):
    temp = None
    if z.ancestor != None:
        temp = z.ancestor

    y = z.left
    t = z.left.right

    y.right = z
    y.right.left = t

    if y.right != None:
        y.right.ancestor = y
    if y.right.left != None:
        y.right.left.ancestor = y.right

    y.ancestor = temp

    return y

def LRRotate(z):
    a = z.left.right
    t = a.left

    a.left = z.left
    a.left.right = t

    a.ancestor = z
    a.left.ancestor = a
    if t != None:
        a.left.right.ancestor = a.left
    
    z.left = a
    return rightRotate(z)

def RLRotate(z):
    a = z.right.left
    t = a.right

    a.right = z.right
    a.right.left = t

    a.ancestor = z
    a.right.ancestor = a
    if a.right.left != None:
        a.right.left.ancestor = a.right
    
    z.right = a
    return leftRotate(z)


def printPostOrder(node):
    if node.left != None:
        printPostOrder(node.left)
    if node.right != None:
        printPostOrder(node.right)
    
    #print(node.data)
    
def getAnsNodes(node, ans_nodes):
    if node.left != None:
        getAnsNodes(node.left, ans_nodes)
    
    ans_nodes.append(node.data)

    if node.right != None:
        getAnsNodes(node.right, ans_nodes)


# construcing AVL tree
for i in range(1, len(inputs)):
    #print(f'Now processing number: {inputs[i]}')
    # check all the balance factor and find critical node
    appendNode(root, inputs[i])

    resultNodes = []
    whichNode = postOrder(root)

    
    # what's the condition
    if len(resultNodes) != 0:
        whichNode = resultNodes[0]
        copy_whichNode = whichNode.create_copy()
        #print(whichNode.data)
        #print(whichNode.balance)
        if whichNode.balance > 1:
            if inputs[i] > whichNode.left.data:
                #print("LR")
                if whichNode.ancestor == None:
                    root = LRRotate(copy_whichNode)
                elif whichNode.data < whichNode.ancestor.data:
                    whichNode.ancestor.left = LRRotate(copy_whichNode)
                else:
                    whichNode.ancestor.right = LRRotate(copy_whichNode)
                operations.append("LR")
            else:
                #print("LL")
                if whichNode.ancestor == None:
                    root = rightRotate(copy_whichNode)
                elif whichNode.data < whichNode.ancestor.data:
                    whichNode.ancestor.left = rightRotate(copy_whichNode)
                else:
                    whichNode.ancestor.right = rightRotate(copy_whichNode)
                operations.append("LL")
        
        if whichNode.balance < -1:
            if inputs[i] < whichNode.right.data:
                #print("RL")
                if whichNode.ancestor == None:
                    root = RLRotate(copy_whichNode)
                elif whichNode.data < whichNode.ancestor.data:
                    whichNode.ancestor.left = RLRotate(copy_whichNode)
                else:
                    whichNode.ancestor.right = RLRotate(copy_whichNode)
                operations.append("RL")
            else:
                #print("RR")
                if whichNode.ancestor == None:
                    #print("no ancestor")
                    root = leftRotate(copy_whichNode)
                elif whichNode.data < whichNode.ancestor.data:
                    #print("smaller than ancestor")
                    whichNode.ancestor.left = leftRotate(whichNode)
                else:
                    #print("greater than ancestor")
                    whichNode.ancestor.right = leftRotate(copy_whichNode)
                    
                operations.append("RR")
    
    printPostOrder(root)
        

def deleteNode(node, num1):
    if num1 == node.data:
        #print(f"Eliminating the target: {num1}")
        if num1 < node.ancestor.data:
            node.ancestor.left = None
        else:
            node.ancestor.right = None
    
    elif num1 < node.data:
        deleteNode(node.left, num1)
    else:
        deleteNode(node.right, num1)

for i in range(len(input_operations)):
    if input_operations[i].split(' ')[0] == "I":
        num1 = int(input_operations[i].split(' ')[1])
        #print(f"Inserting: {num1}")
        #print(f'Now processing number: {num1}')
        # check all the balance factor and find critical node
        appendNode(root, num1)

        resultNodes = []
        whichNode = postOrder(root)

        
        # what's the condition
        if len(resultNodes) != 0:
            whichNode = resultNodes[0]
            copy_whichNode = whichNode.create_copy()
            #print(whichNode.data)
            #print(whichNode.balance)
            if whichNode.balance > 1:
                if inputs[i] > whichNode.left.data:
                    #print("LR")
                    if whichNode.ancestor == None:
                        root = LRRotate(copy_whichNode)
                    elif whichNode.data < whichNode.ancestor.data:
                        whichNode.ancestor.left = LRRotate(copy_whichNode)
                    else:
                        whichNode.ancestor.right = LRRotate(copy_whichNode)
                    operations.append("LR")
                else:
                    #print("LL")
                    if whichNode.ancestor == None:
                        root = rightRotate(copy_whichNode)
                    elif whichNode.data < whichNode.ancestor.data:
                        whichNode.ancestor.left = rightRotate(copy_whichNode)
                    else:
                        whichNode.ancestor.right = rightRotate(copy_whichNode)
                    operations.append("LL")
            
            if whichNode.balance < -1:
                if inputs[i] < whichNode.right.data:
                    #print("RL")
                    if whichNode.ancestor == None:
                        root = RLRotate(copy_whichNode)
                    elif whichNode.data < whichNode.ancestor.data:
                        whichNode.ancestor.left = RLRotate(copy_whichNode)
                    else:
                        whichNode.ancestor.right = RLRotate(copy_whichNode)
                    operations.append("RL")
                else:
                    #print("RR")
                    if whichNode.ancestor == None:
                        #print("no ancestor")
                        root = leftRotate(copy_whichNode)
                    elif whichNode.data < whichNode.ancestor.data:
                        #print("smaller than ancestor")
                        whichNode.ancestor.left = leftRotate(whichNode)
                    else:
                        #print("greater than ancestor")
                        whichNode.ancestor.right = leftRotate(copy_whichNode)
                        
                    operations.append("RR")

    if input_operations[i].split(' ')[0] == "D":
        num1 = int(input_operations[i].split(' ')[1])

        deleteNode(root, num1)
        printPostOrder(root)
        #print("delete done")
        resultNodes = []
        whichNode = postOrder(root, True)
        
        if len(resultNodes) != 0:
            whichNode = resultNodes[0]
            copy_whichNode = whichNode.create_copy()
            #print(f"critical node: {whichNode.data}")

            if num1 < whichNode.data:
                if whichNode.right.balance == 1:
                    #print("R1") # L1
                    # RL
                    if whichNode.ancestor == None:
                        root = RLRotate(copy_whichNode)
                    elif whichNode.data < whichNode.ancestor.data:
                        whichNode.ancestor.left = RLRotate(copy_whichNode)
                    else:
                        whichNode.ancestor.right = RLRotate(copy_whichNode)
                    operations.append("R1")

                elif whichNode.right.balance == 0:
                    #print("R0") # L0
                    # RR
                    if whichNode.ancestor == None:
                        #print("no ancestor")
                        root = leftRotate(copy_whichNode)
                    elif whichNode.data < whichNode.ancestor.data:
                        #print("smaller than ancestor")
                        whichNode.ancestor.left = leftRotate(whichNode)
                    else:
                        #print("greater than ancestor")
                        whichNode.ancestor.right = leftRotate(copy_whichNode)
                    operations.append("R0")
                    
                else:
                    #print("R-1") # L-1
                    # RR
                    if whichNode.ancestor == None:
                        #print("no ancestor")
                        root = leftRotate(copy_whichNode)
                    elif whichNode.data < whichNode.ancestor.data:
                        #print("smaller than ancestor")
                        whichNode.ancestor.left = leftRotate(whichNode)
                    else:
                        #print("greater than ancestor")
                        whichNode.ancestor.right = leftRotate(copy_whichNode)
                    operations.append("R-1")
            else:
                if whichNode.left.balance == 1:
                    #print("R1")
                    # LL
                    if whichNode.ancestor == None:
                        root = rightRotate(copy_whichNode)
                    elif whichNode.data < whichNode.ancestor.data:
                        whichNode.ancestor.left = rightRotate(copy_whichNode)
                    else:
                        whichNode.ancestor.right = rightRotate(copy_whichNode)
                    operations.append("R1")

                elif whichNode.left.balance == 0:
                    #print("R0")
                    # LL
                    if whichNode.ancestor == None:
                        root = rightRotate(copy_whichNode)
                    elif whichNode.data < whichNode.ancestor.data:
                        whichNode.ancestor.left = rightRotate(copy_whichNode)
                    else:
                        whichNode.ancestor.right = rightRotate(copy_whichNode)
                    operations.append("R0")

                else:
                    #print("R-1")
                    # LR
                    if whichNode.ancestor == None:
                        root = LRRotate(copy_whichNode)
                    elif whichNode.data < whichNode.ancestor.data:
                        whichNode.ancestor.left = LRRotate(copy_whichNode)
                    else:
                        whichNode.ancestor.right = LRRotate(copy_whichNode)
                    operations.append("R-1")

    printPostOrder(root)
    #print("round done")


        



ans_nodes = []
#print("\n result tree: ")
getAnsNodes(root, ans_nodes)
for i in range(len(ans_nodes)):
    if i == len(ans_nodes) - 1:
        print(ans_nodes[i])
    else:
        print(ans_nodes[i], end=" ")
print(len(operations))
for i in range(len(operations)):
    if i == len(operations) - 1:
        print(operations[i])
    else:
        print(operations[i], end=",")

