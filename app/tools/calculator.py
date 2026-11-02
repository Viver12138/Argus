import ast
import operator

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def calculate(expression: str) -> float | int:
    """safely evaluate a basic math expression"""

    if not isinstance(expression, str):
        raise TypeError("Expression must be a string")

    if not expression.strip():
        raise ValueError("Expression cannot be empty")

    if len(expression) > 200:
        raise ValueError("Expression is too long")

    def evaluate(node):

        if isinstance(node, ast.Constant):
            if type(node.value) not in (int, float):
                raise ValueError("Only numeric values are allowed")
            return node.value

        if isinstance(node, ast.BinOp):
            operator_type = type(node.op)

            if operator_type not in OPERATORS:
                raise ValueError("Unsupported operator")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if operator_type is ast.Pow and abs(right) > 100:
                raise ValueError("Exponent is too large")

            result = OPERATORS[operator_type](left, right)

            if isinstance(result, (int, float)):
                if abs(result) > 1e100:
                    raise ValueError("Result is too large")

            return result

        if isinstance(node, ast.UnaryOp):
            operator_type = type(node.op)

            if operator_type not in OPERATORS:
                raise ValueError("Unsupported operator")

            return OPERATORS[operator_type](evaluate(node.operand))

        raise ValueError("Unsupported expression")

    try:
        tree = ast.parse(expression, mode="eval")
        return evaluate(tree.body)
    except ZeroDivisionError:
        raise ValueError("Division by zero is not allowed")
    except SyntaxError as exc:
        raise ValueError("Invalid mathematical expression") from exc