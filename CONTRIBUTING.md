# Contributing to Serena

We welcome contributions to Serena! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/serena.git
   cd serena
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install the development dependencies:
   ```bash
   pip install -e .[dev]
   ```

## Development Workflow

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Add tests for your changes
4. Run the test suite:
   ```bash
   pytest
   ```
5. Run code quality checks:
   ```bash
   pyright
   ```
6. Commit your changes:
   ```bash
   git commit -m "Add your commit message"
   ```
7. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
8. Create a pull request on GitHub

## Code Style

- Follow PEP 8 for Python code style
- Use type hints where appropriate
- Write docstrings for public functions and classes
- Keep line length under 120 characters

## Testing

- Write unit tests for new functionality
- Ensure all tests pass before submitting a PR
- Aim for good test coverage

## Documentation

- Update documentation for any new features
- Include examples where helpful
- Update the CHANGELOG.md for significant changes

## Reporting Issues

When reporting issues, please include:

- A clear description of the problem
- Steps to reproduce the issue
- Your environment (OS, Python version, etc.)
- Any relevant error messages or logs

## Feature Requests

We welcome feature requests! Please:

- Check if the feature has already been requested
- Provide a clear description of the feature
- Explain the use case and benefits
- Consider contributing the implementation yourself

## Code of Conduct

Please be respectful and constructive in all interactions. We want to maintain a welcoming environment for all contributors.

## Questions?

If you have questions about contributing, feel free to:

- Open an issue for discussion
- Reach out to the maintainers
- Check our documentation

Thank you for contributing to Serena!