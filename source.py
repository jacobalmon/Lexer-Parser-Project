#Jacob Almon
#Hannah Gonzalez
#Natalie Pedroza

from tkinter import *
import re
from anytree import Node

#math_exp -> key id = math
#math -> multi + multi
#multi -> float * multi | int * multi | float | int

#if_exp -> if(comparison_exp):
#comparison_exp -> id > id

#print_exp -> print("str_literal")

Rowsz = 100
Colsz = 100

def cutOneLineTokens(line):
  output = []
  line = line.replace("\t", "")
  while line != "":
    #checking keywords.
    if re.match(r'(if|else|int|float)', line) != None:
      regexKey = re.match(r'(if|else|int|float)', line)
      keyword = line[regexKey.start():regexKey.end()]
      line = line.replace(keyword, "", 1)
      line = line.strip(' ')
      output.append(f'<key,{keyword}>')

    #checking identifiers.
    elif re.match(r'[a-zA-Z_][a-zA-Z0-9_]*', line) != None:
      regexId = re.match(r'[a-zA-Z_][a-zA-Z0-9_]*', line)
      identifier = line[regexId.start():regexId.end()]
      line = line.replace(identifier, "", 1)
      line = line.strip(' ')
      output.append(f'<id,{identifier}>')

    #checking operators.
    elif re.match(r'(\+|=|\>|\*)', line) != None:
      regexOp = re.match(r'(\+|=|\>|\*)', line)
      operator = line[regexOp.start():regexOp.end()]
      line = line.replace(operator, "", 1)
      line = line.strip(' ')
      output.append(f'<op,{operator}>')

    #checking separators.
    elif re.match(r'(\(|\)|:|"|;)', line) != None:
      regexSep = re.match(r'(\(|\)|:|"|;)', line)
      separator = line[regexSep.start():regexSep.end()]
      line = line.replace(separator, "", 1)
      line = line.strip(' ')
      output.append(f'<sep,{separator}>')

      #we need to check for a ", so strings are picked up as literals, not identifiers.
      if separator == "\"":
        #checking string literals.
        if re.match(r'\b.*\b', line) != None:
          regexLit = re.match(r'\b.*\b', line)
          literal = line[regexLit.start():regexLit.end()]
          line = line.replace(literal, "", 1)
          line = line.strip(' ')
          #we need to check this, in case our literals are capturing empty strings.
          if literal != "":
            output.append(f'<str_lit,{literal}>')

    #checking float literals.
    elif re.match(r'[-]?\d+\.\d+', line) != None:
      regexLit = re.match(r'([-]?\d+\.\d+)', line)
      literal = line[regexLit.start():regexLit.end()]
      line = line.replace(literal, "", 1)
      line = line.strip(' ')
      output.append(f'<float_lit,{literal}>')

    #checking int literals.
    elif re.match(r'[-]?\d+', line) != None:
      regexLit = re.match(r'([-]?\d+)', line)
      literal = line[regexLit.start():regexLit.end()]
      line = line.replace(literal, "", 1)
      line = line.strip(' ')
      output.append(f'<int_lit,{literal}>')
  return output


class LexerParserGUI:

  inToken = [("empty", "empty")]  #reads one token at a time.
  tokens = []  #tokens list.
  numProcessed = 0  #counter for the number of lines being processed.
  itr = "1.0"  #reads line by line from input code.
  parseOutput = ""  #output string for parse tree sentences.
  flag = False  #flag for tree implementation.

  def __init__(self, root):
    #Window Name.
    self.master = root
    self.master.geometry("950x700")
    blankspace = " "
    self.master.title(30 * blankspace + "Lexer & Parser for TinyPie")

    #Label for Input Source Code.
    self.input = Label(self.master, text="Source Code")
    self.input.place(x=30, y=25)

    #Label for Result.
    self.output = Label(self.master, text="Tokens")
    self.output.place(x=345, y=25)

    #Text Box for Input.
    self.inputCode = Text(self.master, height=16, width=40)
    self.inputCode.place(x=30, y=50)

    #Text Box for Output.
    self.outputCode = Text(self.master, height=16, width=40)
    self.outputCode.place(x=345, y=50)

    #Line Processing.
    self.lineProcessing = Label(self.master, text="Current Line Processing: ")
    self.lineProcessing.place(x=30, y=615)

    #Next Line Button.
    self.nextLine = Button(self.master,
                           text=blankspace * 5 + "Next Line" + 5 * blankspace,
                           command=self.submitLine,
                           bg="lightblue")
    self.nextLine.place(x=30, y=650)

    #Quit Button
    self.quit = Button(self.master,
                       text=blankspace * 5 + "EXIT" + 5 * blankspace,
                       command=self.master.destroy,
                       bg="lightblue")
    self.quit.place(x=850, y=650)

    #Line Counter
    self.numProcessedLines = Label(self.master, text=self.numProcessed)
    self.numProcessedLines.place(x=190, y=615)

    #Label for Parser.
    self.parseLabel = Label(self.master, text="Parse Tree")
    self.parseLabel.place(x=660, y=25)

    #Text Box for Parser.
    self.parseText = Text(self.master, height=16, width=40)
    self.parseText.place(x=660, y=50)

    self.pwrapper = ParseTreeWrapper()
    self.viewer = TreeViewer(self.pwrapper, self.master)

  def submitLine(self):
    self.numProcessed += 1
    temp = self.inputCode.get(self.itr, "end")

    #updates lineCounter.
    self.itr = self.itr.strip(".0")
    self.itr = int(self.itr)
    self.itr += 1
    self.itr = str(self.itr)
    self.itr += ".0"

    #helper for substringing later.
    counter = 0
    for i in temp:
      if i == "\n":
        break
      else:
        counter += 1

    #substringing everything.
    oneLine = temp[0:counter + 1]
    oneLine = oneLine.strip("\n")
    self.tokens = cutOneLineTokens(oneLine)
    temp2 = ""
    for i in self.tokens:
      temp2 += i
      temp2 += '\n'

    #inserts at the end of the text box for lexer.
    self.outputCode.insert("end", temp2)

    #Insert output into text box foe tokens
    self.numProcessedLines = Label(self.master, text=self.numProcessed)
    self.numProcessedLines.place(x=190, y=615)

    #formatting each element into a list of tuples.
    newTokens = []
    for i in self.tokens:
      temp1 = i.find(',')
      type = i[1:temp1]
      token = i[temp1 + 1:-1]
      newTuple = (type, token)
      newTokens.append(newTuple)
    self.tokens = newTokens

    #creates parse tree for line being processed.
    self.parser()

    #inserts at the end of the text box for parser.
    self.parseText.insert("end", self.parseOutput)
    self.parseOuput = ""

  def parser(self):
    self.inToken = self.tokens.pop(0)
    if self.inToken[1] == "if":
      self.if_exp()
      self.viewer.updateTree(self.pwrapper.root)
      if self.inToken[1] == ':':
        self.parseOutput += "\nparse tree building success"

    elif self.inToken[0] == "key":
      self.math_exp()
      self.viewer.updateTree(self.pwrapper.root)

    elif self.inToken[0] == "id" and self.inToken[1] == "print":
      self.print_exp()
      self.viewer.updateTree(self.pwrapper.root)

    if self.inToken[1] == ';':
      self.parseOutput += "\nparse tree building success"

    return

  def accept_token(self):
    #pops an element from our list, token is processed.
    self.parseOutput += "\n     accept token from the list: " + self.inToken[1]
    self.inToken = self.tokens.pop(0)

  def math_exp(self):
    self.mathExpParseTree = Node("math_exp")
    self.pwrapper.root = self.mathExpParseTree
    self.parseOutput += "\n----parent node math_exp, finding children nodes:"

    #checking for first element to be a keyword.
    if self.inToken[0] == "key":
      self.keyNode = Node("keyword", parent=self.mathExpParseTree)
      self.keyNameNode = Node(f"{self.inToken[1]}", parent=self.keyNode)
      self.parseOutput += "\nchild node (internal): keyword"
      self.parseOutput += "\n   keyword has child node (token): " + self.inToken[
          1]
      self.accept_token()

    else:
      self.parseOutput += "expect keyword as the first element of the expression!\n"
      return

    #checking for second element to be identifier.
    if self.inToken[0] == "id":
      self.idNode = Node("identifier", parent=self.mathExpParseTree)
      self.idNameNode = Node(f"{self.inToken[1]}", parent=self.idNode)
      self.parseOutput += "\nchild node (internal): identifier"
      self.parseOutput += "\n   identifier has child node (token): " + self.inToken[
          1]
      self.accept_token()

    else:
      self.parseOutput += "\nexpect identifier as the second element of the expression!\n"
      return

    #checking for third element to be =.
    if self.inToken[1] == '=':
      self.equalNode = Node("=", parent=self.mathExpParseTree)
      self.parseOutput += "\nchild node (token): " + self.inToken[1]
      self.accept_token()

    else:
      self.parseOutput += "\nexpect = as the third element of the expression!"
      return

    #meets our bnf grammar for math_exp.
    self.parseOutput += "\nChild node (internal): math"
    self.math()

  def math(self):
    self.mathNode = Node("math", parent=self.mathExpParseTree)
    self.parseOutput += "\n----parent node math, finding children nodes: "

    #checking for first element to be a int or float for multi.
    if self.inToken[0] == "float_lit" or self.inToken[0] == "int_lit":
      #meets bnf grammar for math on the left side.
      self.parseOutput += "\nchild node (multi): "
      self.multi()

    else:
      self.parseOutput += "\nexpect float_lit or int_lit as the first element of the expression!"
      return

    self.parseOutput += "\n----continuing parent node math, finding children nodes:"

    #checking for second element to be +.
    if self.inToken[1] == "+":
      self.addNode = Node("+", parent=self.mathNode)
      self.parseOutput += "\nchild node (token): " + self.inToken[1]
      self.accept_token()

    else:
      self.parseOutput += "\nexpect + as the second element of the expression!"
      return

    #checking for third element to be a float or int for multi.
    if self.inToken[0] == "float_lit" or self.inToken[0] == "int_lit":
      #meets bnf grammar for math on the right side.
      self.parseOutput += "\nchild node (multi):"
      self.flag = False
      self.multi()

    else:
      self.parseOutput += "\nexpect float_lit or int_lit as the third element of the expression!"
      return

  def multi(self):
    if self.flag == True:
      self.recMultiNode = Node("multi", parent=self.multiNode)
    else:
      self.multiNode = Node("multi", parent=self.mathNode)
    self.parseOutput += "\n----parent node multi, finding children nodes:"

    #checking for first element to be a float
    if self.inToken[0] == "float_lit":
      if self.flag == True:
        self.float1Node = Node("float_lit", parent=self.recMultiNode)
      else:
        self.float1Node = Node("float_lit", parent=self.multiNode)
      self.floatLit1Node = Node(f"{self.inToken[1]}", parent=self.float1Node)
      self.parseOutput += "\nchild node (internal): float_lit"
      self.parseOutput += "\n   float_lit has child node (token):" + self.inToken[
          1]
      self.accept_token()

      #checking for second element to be *, not required.
      if self.inToken[1] == "*":
        self.multiply1Node = Node("*", parent=self.multiNode)
        self.parseOutput += "\nchild node (token):" + self.inToken[1]
        self.accept_token()
        self.parseOutput += "\nchild node (internal): multi"
        self.flag = True
        self.multi()

    #checking for first element to be a int
    elif self.inToken[0] == "int_lit":
      if self.flag == True:
        self.int1Node = Node("int_lit", parent=self.recMultiNode)
      else:
        self.int1Node = Node("int_lit", parent=self.multiNode)
      self.intLit1Node = Node(f"{self.inToken[1]}", parent=self.int1Node)
      self.parseOutput += "\nchild node (internal): int"
      self.parseOutput += "\n   int_lit has child node (token):" + self.inToken[
          1]
      self.accept_token()

      #checking for second element to be *, not required.
      if self.inToken[1] == "*":
        self.multiply2Node = Node("*", parent=self.multiNode)
        self.parseOutput += "\nchild node (token):" + self.inToken[1]
        self.accept_token()
        self.parseOutput += "\nchild node (internal): multi"
        self.flag = True
        self.multi()

    else:
      self.parseOutput += "\nexpect float_lit or int_lit as the first or third element in the expression!"
      return
    self.flag = False

  def if_exp(self):

    self.ifExpParseTree = Node("if_exp")
    self.pwrapper.root = self.ifExpParseTree
    self.parseOutput += "\n----parent node if_exp, finding children nodes"

    #checking the first element is if, then add to parseOutput
    if self.inToken[1] == "if":
      self.ifNode = Node("if", self.ifExpParseTree)
      self.parseOutput += "\nchild node(internal): if"
      self.parseOutput += "\n   float_lit has child node (token):" + self.inToken[1]
      self.accept_token()

    else:
      self.parseOutput += "\nexpect if as the first element in the expression!"
      return

    #checking for ( , then add to parseOutput
    if self.inToken[1] == "(":
      self.sep1Node = Node("(", self.ifExpParseTree)
      self.parseOutput += "\n child node (internal): ("
      self.accept_token()
      #if matched call comparison_exp.
      self.comparison_exp()
    else:
      self.parseOutput += "\nexpect ( as the second element in the expression!"
      return

    #checking for ) , then add to parseOutput
    if self.inToken[1] == ")":
      self.sep2Node = Node(")", self.ifExpParseTree)
      self.parseOutput += "\n child node (internal): )"
      self.accept_token()
      #if all met, then it meets the bnf grammer.
    else:
      self.parseOutput += "\nexpect ) as the third element in the expression!"
      return

  def comparison_exp(self):
    self.compExpNode = Node("comp_exp", parent=self.ifExpParseTree)
    self.parseOutput += "\n----parent node comparison_exp, finding children nodes"

    #checking for id, then add to parseOutput
    if self.inToken[0] == "id":
      self.id1Node = Node("identifier", parent=self.compExpNode)
      self.name1Node = Node(f'{self.inToken[1]}', parent=self.id1Node)
      self.parseOutput += "\nchild node (internal): identifier"
      self.parseOutput += "\n   identifier has child node (token): " + self.inToken[1]
      self.accept_token()

    else:
      self.parseOutput += "\nexpect id as the first element in the expression!"
      return

    #checking for >, then add to parseOutput
    if self.inToken[1] == ">":
      self.greaterNode = Node(">", parent=self.compExpNode)
      self.parseOutput += "\nchild node (internal): >"
      self.accept_token()

    else:
      self.parseOutput += "\nexpect > as the second element in the expression!"
      return

    #checking for id, then add to parseOutput
    if self.inToken[0] == "id":
      self.id2Node = Node("identifier", parent=self.compExpNode)
      self.name2Node = Node(f'{self.inToken[1]}', parent=self.id2Node)
      self.parseOutput += "\nchild node (internal): identifier"
      self.parseOutput += "\n   identifier has child node(token): " + self.inToken[1]
      self.accept_token()
    #if all met, then it meets the bnf grammer
    else:
      self.parseOutput += "\nexpect id as the third element in the expression!"
      return

  def print_exp(self):
    self.printParseTree = Node("print_exp")
    self.pwrapper.root = self.printParseTree
    self.parseOutput += "\n----parent node print_exp, finding children nodes:"

    #no need to check if the token is <id, print>, since we checked it in parser().
    self.printNode = Node("print", parent=self.printParseTree)
    self.parseOutput += "\nchild node (internal): identifier"
    self.parseOutput += "\n   identifier has child node (token):" + self.inToken[
        1]
    self.accept_token()

    #checking for second element to be (.
    if self.inToken[1] == '(':
      self.sep3Node = Node("(", parent=self.printParseTree)
      self.parseOutput += "\nchild node (token): " + self.inToken[1]
      self.accept_token()

    else:
      self.parseOutput += "\nexpect ( as the second element in the expression!"
      return

    #checking for third element to be ".
    if self.inToken[1] == '\"':
      self.sep4Node = Node('\"', parent=self.printParseTree)
      self.parseOutput += "\nchild node (token): \""
      self.accept_token()

    else:
      self.parseOutput += "\nexpect \" as the third element in the expression!"
      return

    #checking for fourth element to be str_lit.
    if self.inToken[0] == "str_lit":
      self.strLitNode = Node("str_lit", parent=self.printParseTree)
      self.stringNode = Node(f'{self.inToken[1]}', self.strLitNode)
      self.parseOutput += "\nchild node (internal): str_lit"
      self.parseOutput += "\n   str_lit has child node (token):" + self.inToken[1]
      self.accept_token()

    else:
      self.parseOutput += "\nexpect str_lit as the fourth element in the expression!"
      return

    #checking for the fifth element to be ".
    if self.inToken[1] == '\"':
      self.sep5Node = Node('\"', parent=self.printParseTree)
      self.parseOutput += "\nchild node (token): \""
      self.accept_token()

    else:
      self.parseOutput += "\nexpect \" as the fifth element in the expression!"
      return

    #checking sixth element to be ).
    if self.inToken[1] == ')':
      self.sep6Node = Node(')', parent=self.printParseTree)
      self.parseOutput += "\nchild node (token): )"
      self.accept_token()

    else:
      self.parseOutput += "\nexpect ) as the sixth element in the expression!"
      return


#Hannah
class TreeViewer(Frame):

  def __init__(self, wrapper, parent=None, tree=None):
    Frame.__init__(self, parent)
    self.makeWidgets()
    self.wrapper = wrapper
    if tree:
      self.drawTree(tree)

  
  def makeWidgets(self):
    #Label for Tree Visualization.
    self.treeLabel = Label(self.master, text="Tree Visualization")
    self.treeLabel.place(x=30, y=320)

    #Output Box for Tree Visualization.
    self.canvas = Canvas(self.master, height=220, width=920, bg="white")
    self.canvas.place(x=30, y=350)

    #Vertical Scrollbar
    self.vertbar = Scrollbar(self.canvas, orient=VERTICAL)
    self.vertbar.place(x=910, y=0, height=225)
    self.vertbar.config(command=self.canvas.yview)
    self.canvas.config(yscrollcommand=self.vertbar.set)

    # Configure Canvas to work with Scrollbars.
    self.canvas.bind(
        '<Configure>',
        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

  def clearTree(self):
    self.canvas.delete('all')

  def drawTree(self, tree):
    self.clearTree()
    wrapper = self.wrapper
    self.updateTree(wrapper.root)

  def updateTree(self, root):
    self.clearTree()
    levels, maxrow = self.planLevels(root, self.wrapper)
    self.canvas.config(scrollregion=(0, 0, (Colsz * maxrow),
                                     (Rowsz * len(levels))))
    self.drawLevels(levels, maxrow, self.wrapper)

  def planLevels(self, root, wrap):
    levels = []
    maxrow = 0
    currlevel = [(root, None)]
    while currlevel:
      levels.append(currlevel)
      size = len(currlevel)
      if size > maxrow:
        maxrow = size
      nextlevel = []
      for (node, parent) in currlevel:
        if node is not None:
          children = wrap.children(node)
          if not children:
            nextlevel.append((None, None))
          else:
            for child in children:
              nextlevel.append((child, node))
      currlevel = nextlevel
    return levels, maxrow

  def drawLevels(self, levels, maxrow, wrap):
    node_positions = {}
    rowpos = 0
    for level in levels:
      colinc = (maxrow * Colsz) / (len(level) + 1)
      colpos = 0
      for (node, parent) in level:
        colpos += colinc-3
        if node is not None:
          text = wrap.label(node)
          more = wrap.value(node)
          if more:
            text = text + '=' + more
          win = Label(self.canvas, text=text, relief=RAISED)
          win.pack()
         
          box_width = Colsz * 0.75
          box_height = Rowsz * 0.5

          self.canvas.create_window(colpos, rowpos, anchor="nw", window=win, width=box_width, height=box_height)

          if parent is not None:
            parent_pos = node_positions.get(parent, (0,0))
            line_start = (parent_pos[0] + box_width * 0.25, parent_pos[1] + box_height)
            line_end = (colpos + box_width * 0.5, rowpos)

          # draw a line connecting parent and child (start: column pos, row pos, end: column pos, row pos)
            self.canvas.create_line(line_start[0], line_start[1], line_end[0], line_end[1], arrow='last', width=1)

          # save the child's position for future reference
          node_positions[node] = (colpos, rowpos)
          
        colpos += 0.25
      rowpos += Rowsz


class ParseTreeWrapper:

  def __init__(self):
    self.root = None

  def children(self, node):
    return node.children

  def addChild(self, parent, child):
    child.parent = parent

  def label(self, node):
    return str(node.name)

  def value(self, node):
    return None


if __name__ == "__main__":
  myTkRoot = Tk()
  myGui = LexerParserGUI(myTkRoot)
  myTkRoot.mainloop()