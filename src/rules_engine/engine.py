from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Iterable, List, Optional


@dataclass(frozen=True)
class RuleViolation:
    rule_type: str
    message: str
    code: Optional[str] = None
    related_code: Optional[str] = None


@dataclass
class ValidationReport:
    violations: List[RuleViolation]

    @property
    def is_valid(self) -> bool:
        return not self.violations


class TardocRulesEngine:
    """Declarative rules engine for TARDOC combinations."""

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def validate_combination(self, codes: Iterable[str]) -> ValidationReport:
        code_list = list(dict.fromkeys(codes))
        violations: List[RuleViolation] = []
        if not code_list:
            return ValidationReport(violations=[RuleViolation("input", "No codes provided")])

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            code_rows = self._fetch_codes(conn, code_list)
            missing = sorted(set(code_list) - {row["code"] for row in code_rows})
            for code in missing:
                violations.append(RuleViolation("missing_code", f"Code {code} not found", code=code))

            if missing:
                return ValidationReport(violations)

            code_ids = {row["code"]: row["id"] for row in code_rows}

            violations.extend(self._check_exclusions(conn, code_ids))
            violations.extend(self._check_incompatibilities(conn, code_ids))
            violations.extend(self._check_conditions(conn, code_ids))
            violations.extend(self._check_limits(conn, code_ids))

        return ValidationReport(violations)

    def _fetch_codes(self, conn: sqlite3.Connection, codes: List[str]) -> List[sqlite3.Row]:
        placeholders = ",".join("?" for _ in codes)
        query = f"SELECT id, code FROM codes WHERE code IN ({placeholders})"
        return list(conn.execute(query, codes))

    def _check_exclusions(self, conn: sqlite3.Connection, code_ids: dict[str, int]) -> List[RuleViolation]:
        violations: List[RuleViolation] = []
        for code, code_id in code_ids.items():
            rows = conn.execute(
                "SELECT excluded_code, reason FROM exclusions WHERE code_id = ?",
                (code_id,),
            )
            for row in rows:
                if row["excluded_code"] in code_ids:
                    violations.append(
                        RuleViolation(
                            "exclusion",
                            row["reason"] or f"{code} excludes {row['excluded_code']}",
                            code=code,
                            related_code=row["excluded_code"],
                        )
                    )
        return violations

    def _check_incompatibilities(self, conn: sqlite3.Connection, code_ids: dict[str, int]) -> List[RuleViolation]:
        violations: List[RuleViolation] = []
        for code, code_id in code_ids.items():
            rows = conn.execute(
                """
                SELECT c2.code AS incompatible_code, i.reason
                FROM incompatibilities i
                JOIN codes c2 ON c2.id = i.code_id_b
                WHERE i.code_id_a = ?
                """,
                (code_id,),
            )
            for row in rows:
                if row["incompatible_code"] in code_ids:
                    violations.append(
                        RuleViolation(
                            "incompatibility",
                            row["reason"] or f"{code} incompatible with {row['incompatible_code']}",
                            code=code,
                            related_code=row["incompatible_code"],
                        )
                    )
        return violations

    def _check_conditions(self, conn: sqlite3.Connection, code_ids: dict[str, int]) -> List[RuleViolation]:
        violations: List[RuleViolation] = []
        for code, code_id in code_ids.items():
            rows = conn.execute(
                "SELECT expression, message FROM conditions WHERE code_id = ?",
                (code_id,),
            )
            for row in rows:
                if not self._evaluate_expression(row["expression"], code_ids):
                    violations.append(
                        RuleViolation(
                            "condition",
                            row["message"] or f"Condition failed for {code}",
                            code=code,
                        )
                    )
        return violations

    def _check_limits(self, conn: sqlite3.Connection, code_ids: dict[str, int]) -> List[RuleViolation]:
        violations: List[RuleViolation] = []
        for code, code_id in code_ids.items():
            rows = conn.execute(
                "SELECT limit_type, value, period, message FROM limits WHERE code_id = ?",
                (code_id,),
            )
            for row in rows:
                if row["limit_type"] == "max_occurrences":
                    if row["value"] < 1:
                        violations.append(
                            RuleViolation(
                                "limit",
                                row["message"] or f"Limit reached for {code}",
                                code=code,
                            )
                        )
        return violations

    def _evaluate_expression(self, expression: str, code_ids: dict[str, int]) -> bool:
        """Minimal expression evaluator.

        Supported syntax:
        - `has(CODE)`
        - `not has(CODE)`
        - `has(CODE_A) and has(CODE_B)`
        - `has(CODE_A) or has(CODE_B)`
        """
        tokens = expression.replace("(", " ").replace(")", " ").split()
        eval_tokens: List[str] = []
        for token in tokens:
            if token.startswith("has(") and token.endswith(")"):
                code = token[4:-1]
                eval_tokens.append(str(code in code_ids))
            elif token.lower() in {"and", "or", "not"}:
                eval_tokens.append(token.lower())
            else:
                eval_tokens.append(token)
        try:
            return bool(eval(" ".join(eval_tokens)))  # noqa: S307
        except (SyntaxError, NameError):
            return False
