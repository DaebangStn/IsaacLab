# IsaacLab Development Guide

## Core Tools
- Python 3.10 with line length 120
- `./isaaclab.sh --format` - Run code formatting (uses pre-commit)
- `./isaaclab.sh --install` - Install extensions and dependencies
- `./isaaclab.sh --test` - Run all tests
- `./isaaclab.sh -p tools/run_all_tests.py` - Test with options
- `./isaaclab.sh -p path/to/single_test.py` - Run single test

## Code Style
- Black formatter (120 line length)
- Google Style Guide (https://google.github.io/styleguide/pyguide.html)
- Type hints in function signatures (not in docstrings)
- isort for imports with specific ordering (see pyproject.toml)
- flake8 with additional linters (simplify, return)

## Documentation
- Google-style docstrings for functions/classes
- Document what, why, and how (not just what)
- Sphinx for building (`./isaaclab.sh --docs`)

## Testing
- Use unittest framework
- Tests live in source/*/test/ directories