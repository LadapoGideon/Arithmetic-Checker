"""Find arithmetic claims in text such as "12 * 4 = 48" and check whether they are correct."""
import ast
import operator
import re

CLAIM_PATTERN = re.compile(r"([0-9(][0-9+\-*/(). ]*?)\s*=\s*(-?\d+(?:\.\d+)?)")

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def safe_eval(expression):
    """Evaluate a plain arithmetic expression. Anything else raises ValueError."""
    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](evaluate(node.left), evaluate(node.right))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -evaluate(node.operand)
        raise ValueError("unsupported expression")

    return evaluate(ast.parse(expression.strip(), mode="eval"))


def check_arithmetic(text, tolerance=1e-9):
    """
    Returns a list of dicts for each claim found:
    {"expression", "claimed", "actual", "correct"}.
    If the expression cannot be evaluated, "correct" is None and "error" explains why.
    """
    findings = []
    for match in CLAIM_PATTERN.finditer(text):
        expression = match.group(1).strip()
        claimed = float(match.group(2))
        try:
            actual = safe_eval(expression)
        except (ValueError, SyntaxError, ZeroDivisionError) as err:
            findings.append({"expression": expression, "claimed": claimed, "actual": None,
                             "correct": None, "error": str(err)})
            continue
        findings.append({"expression": expression, "claimed": claimed, "actual": actual,
                         "correct": abs(actual - claimed) <= tolerance})
    return findings


def wrong_claims(text):
    return [f for f in check_arithmetic(text) if f["correct"] is False]
