"""Disposable fixture for a real FAS CI-recovery run."""


def add(a: int, b: int) -> int:
    # Intentional defect: the live recovery agent must identify and fix this.
    return a - b
