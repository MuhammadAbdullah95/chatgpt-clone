"""One folder per feature.

Each feature follows the same pattern: router.py (HTTP only) -> service.py (logic)
-> repository.py (database), plus models.py and schemas.py when needed.
Features talk to each other only through service.py.
"""
