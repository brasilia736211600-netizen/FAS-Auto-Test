"""Bounded model fallback for portable FAS execution."""
from __future__ import annotations

import subprocess
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass

from model_router import RouteDecision


@dataclass(frozen=True)
class ModelAttempt:
    model: str
    returncode: int
    duration_seconds: float


@dataclass(frozen=True)
class FallbackResult:
    success: bool
    selected_model: str | None
    attempts: tuple[ModelAttempt, ...]


def run_with_fallback(
    command_factory: Callable[[str], Sequence[str]],
    candidates: Sequence[str],
    *,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    cwd: str | None = None,
    max_attempts: int = 3,
) -> FallbackResult:
    """Try distinct model candidates with a hard attempt bound.

    The runner is injectable for deterministic tests. No retry occurs after the
    bound and the first successful model is retained as the effective model.
    """
    if not candidates:
        raise ValueError("at least one model candidate is required")
    if max_attempts < 1:
        raise ValueError("max_attempts must be positive")

    attempts: list[ModelAttempt] = []
    seen: set[str] = set()
    for model in candidates:
        if model in seen:
            continue
        seen.add(model)
        if len(attempts) >= max_attempts:
            break
        start = time.monotonic()
        completed = runner(command_factory(model), cwd=cwd, check=False, text=True)
        duration = time.monotonic() - start
        attempts.append(ModelAttempt(model, completed.returncode, duration))
        if completed.returncode == 0:
            return FallbackResult(True, model, tuple(attempts))

    return FallbackResult(False, None, tuple(attempts))


def candidate_models(decision: RouteDecision, fallback_models: Sequence[str]) -> tuple[str, ...]:
    """Put the routed model first, then unique configured fallbacks."""
    return tuple(dict.fromkeys((decision.model, *fallback_models)))
