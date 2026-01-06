# Moteur de règles TARDOC

## Interface
`TardocRulesEngine` expose `validate_combination(codes)` et retourne un `ValidationReport`.

## Expressions supportées
- `has(CODE)`
- `not has(CODE)`
- `has(CODE_A) and has(CODE_B)`
- `has(CODE_A) or has(CODE_B)`

## Exemple
```python
from rules_engine.engine import TardocRulesEngine

engine = TardocRulesEngine("data/tardoc/tardoc.db")
report = engine.validate_combination(["A100", "B200"])
print(report.is_valid)
```
