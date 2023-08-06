import glob
import os
import re
from lxml import etree

from ActionClasses import DummyOperatorObject,PythonBranchOperator
from DAG import DAG
from MappingNodes import Traverse
from DependencyFlow import DependencyFlow
from StartingNode import StartingNode
from UndefinedNodes import Undefined

arr = []

global cnt


##checking dependency

# MAIN

def process_file(xmlfile, queue,output_dir):
    ## xml file is parsed
    parser = etree.XMLParser(remove_comments=True)
    tree = etree.parse(xmlfile,parser)
    ## root contains all the workflow nodes in parsed xml node
    root = tree.getroot()
    ## to get the name of the parsed xml file
    dagname = root.base[root.base.rfind("/") + 1:].strip(".xml")
    ## create object of the DAG class in DAG.py 
    dag = DAG()
    ## queue name is passed as input by the user
    queue = queue
    dag._dagname = dagname
    child = []
    mylist=[]
    dagarr=[]
    # child array stored all the nodes in the XML file
    for child_count in range(len(root)):
        child.append(root[child_count])
    
    ## we check the tags of the nodes present in child array
    for i in range(len(child)):
        print(child[i].tag)
    
    ## the dag and the child array is passed to the startingnode and then the returned value is stored in string1
    start_node=StartingNode(child,dag,queue)
    string1=start_node.starting_node()

    ## recursion starts, by passing the value of the node that start element points to.
    #dependency_flow(child,dag,string1,mylist,dagarr,queue)
    depend=DependencyFlow(child,dag,string1,mylist,dagarr,queue)
    depend.dependency_flow()
    #print("dag sequence is: ",dag.sequence,"\n\n")

    ## create object of the Traverse class
    node1=Traverse(dag,queue,root,dagname)
    ## call the node_traversal method which will append all the mapped ozzie nodes to the python file
    node1.node_traversal()  
    print("tracknodes is:",dag.tracknode)
    no_elem=[]
    undefined=Undefined(dag,queue,no_elem)
    undefined.undefined_nodes()

    ## currently textforvar, variable_pattern and vars is redundant as they were used for defining the default args 
    ## but instead we are reading configuration file using: dag_run.conf['']
    textforvars = open(xmlfile, "r").read()
    variable_pattern = re.compile(r'\$\{(\w+)\}')
    vars = set(variable_pattern.findall(textforvars))
    print(dag.create_dag_file(vars, os.path.join(output_dir,xmlfile.replace(".xml", ".py")),queue))

# class conversion:
#     def __init__(self,input_dir,output_dir,queue):
#         self.input_dir=input_dir
#         self.output_dir=output_dir
#         self.queue=queue
def conversion(input_dir,output_dir,queue):
        os.chdir(input_dir)
        for file in glob.glob("*.xml"):
            process_file(file, queue,output_dir)

# conv=conversion(input_dir)
# conv.conversion_main()

