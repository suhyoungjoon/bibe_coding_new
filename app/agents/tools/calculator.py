import ast, operator as op
OPS = { ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv, ast.Pow: op.pow, ast.USub: op.neg }
def _eval(node):
    if isinstance(node, ast.Num): return node.n
    elif isinstance(node, ast.BinOp): return OPS[type(node.op)](_eval(node.left), _eval(node.right))
    elif isinstance(node, ast.UnaryOp): return OPS[type(node.op)](_eval(node.operand))
    else: raise TypeError(node)
def safe_calculate(expr: str):
    tree = ast.parse(expr, mode="eval"); return _eval(tree.body)
