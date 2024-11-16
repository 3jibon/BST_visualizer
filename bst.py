import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
import copy

class Node:
    def __init__(self,data):
        self.left=None
        self.data=data
        self.right=None
class Tree:
    def __init__(self):
        self.frames=[]
    def buildTree(self,valList):
        root=Node(valList[0])
        for i in range(1,len(valList)):
            self.insertNode(root,valList[i])
            self.frames.append(copy.deepcopy(root))
        return root
    def insertNode(self,root,data):
        if root is None:
            return Node(data)
        if root.data>data:
            root.left=self.insertNode(root.left,data)
        if root.data<data:
            root.right=self.insertNode(root.right,data)
        return root
    def find_co_ordinates(self,root,pos=None,x=0,y=0,width=2):
        if pos is None:
            pos={}
        pos[root.data]=(x,y)
        if root.left:
            pos=self.find_co_ordinates(root.left,pos=pos,x=x-width,y=y-1,width=width/2)
        if root.right:
            pos=self.find_co_ordinates(root.right,pos=pos,x=x+width,y=y-1,width=width/2)
        return pos
    def draw_BST(self,root):
        pos=self.find_co_ordinates(root)
        G=nx.Graph()

        def add_edges(root):
            if root.left:
                G.add_edge(root.data,root.left.data)
                add_edges(root.left)
            if root.right:
                G.add_edge(root.data,root.right.data)
                add_edges(root.right)

        add_edges(root)

        return G,pos
def animation(valList):
    tree = Tree()
    tree.buildTree(valList)
    fig, ax = plt.subplots(figsize=(7, 7))

    def animate(i):
        ax.clear()
        frame=tree.frames[i]
        G, pos = tree.draw_BST(frame)

        node_colors=['skyblue']*len(G.nodes)

        current_node = valList[i+1]
        node_colors[list(G.nodes).index(current_node)] = 'lightgreen'

        edge_colors = ['gray'] * len(G.edges)
        for u, v in G.edges:
            if v == current_node:
                edge_colors[list(G.edges).index((u, v))] = 'red'
                break

        nx.draw(G, pos, with_labels=True, node_size=3000, node_color=node_colors,
                font_size=10, font_weight="bold", edge_color=edge_colors)
        ax.set_title(f"Binary search Tree\nstep{i+2}: Insert{valList[i+1]}")

    ani = FuncAnimation(fig, animate, frames=len(tree.frames), repeat=False, interval=3000)
    plt.show()       

def main():
    valList = list(map(int, input("Enter values for the BST (space-separated): ").split()))
    animation(valList)

if __name__=="__main__":
    main()