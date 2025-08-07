# Contributing to Tempo

Thank you for your interest in contributing to Tempo! We welcome contributions from everyone.

## Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/tempo.git
   cd tempo
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -e .[dev]
   ```

## Development Process

We follow Test-Driven Development (TDD) strictly:

### Red-Green-Refactor Cycle

1. **RED**: Write a failing test first
2. **GREEN**: Write minimal code to make the test pass
3. **REFACTOR**: Improve the code while keeping tests green

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/unit/core/test_tracker.py

# Run in watch mode
pytest-watch
```

### Code Coverage

- Minimum 80% coverage required
- Current coverage: 89%
- New features must include tests

## Pull Request Process

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following TDD
3. Ensure all tests pass
4. Update documentation if needed
5. Commit with clear messages:
   ```bash
   git commit -m "Add feature: description of what you added"
   ```

6. Push to your fork and create a Pull Request

## Code Style

- Follow PEP 8
- Use type hints where appropriate
- Keep functions small and focused
- Write clear docstrings

## Reporting Issues

- Use GitHub Issues
- Include steps to reproduce
- Provide system information (OS, Python version)
- Include error messages if applicable

## Feature Requests

- Open an issue with "Feature Request" label
- Describe the use case
- Explain expected behavior
- Consider implementing it yourself!

## Testing Guidelines

### Test Structure
```python
def test_component_action_expected_result():
    # Arrange
    setup_test_data()
    
    # Act
    result = perform_action()
    
    # Assert
    assert result == expected_value
```

### Test Requirements
- Fast execution (< 100ms for unit tests)
- Independent (no test dependencies)
- Clear naming
- Good coverage of edge cases

## Documentation

- Update README.md for user-facing changes
- Update ROADMAP.md for progress tracking
- Add docstrings to all public functions
- Include usage examples

## Questions?

Feel free to open an issue for any questions about contributing!