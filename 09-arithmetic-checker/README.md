# Arithmetic Reasoning Checker

Step-by-step answers from language models often include small calculation errors that look convincing. This tool finds statements like `12 * 4 = 48` in a response and checks each one.

It evaluates the math with a restricted parser, not Python's `eval()`, so it cannot run arbitrary code.

**Skills shown:** checking reasoning steps, safe expression parsing, handling edge cases such as division by zero.

## Run the tests

```
python3 -m unittest -v
```

## Example

```python
from arithmetic_check import wrong_claims

for finding in wrong_claims(model_answer):
    print(finding["expression"], "should equal", finding["actual"])
```

## Limits

It only catches claims written in the form `expression = result`. Word problems that never write out the equation are not checked.
