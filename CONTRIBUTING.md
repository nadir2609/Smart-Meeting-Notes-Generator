# Contributing to Smart Meeting Notes Generator

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/smart-meeting-notes/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)
   - Error messages/logs

### Suggesting Features

1. Check existing [Issues](https://github.com/yourusername/smart-meeting-notes/issues) for similar suggestions
2. Create a new issue with:
   - Clear feature description
   - Use case and benefits
   - Possible implementation approach

### Pull Requests

1. **Fork** the repository
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**:
   - Write clear, commented code
   - Follow existing code style
   - Add tests if applicable
4. **Test your changes**:
   ```bash
   pytest  # Run tests
   ```
5. **Commit** with clear messages:
   ```bash
   git commit -m "Add feature: description"
   ```
6. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request** with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots (if UI changes)

## Code Style

- Follow PEP 8 for Python code
- Use type hints where possible
- Add docstrings to functions/classes
- Keep functions focused and small
- Use meaningful variable names

## Development Setup

```bash
# Clone your fork
git clone https://github.com/nadir2609/Smart-Meeting-Notes-Generator.git
cd Smart-Meeting-Notes-Generator

# Create virtual environment
python -m venv env
source env/bin/activate  # or .\env\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8

# Run tests
pytest

# Format code
black .

# Check linting
flake8 .
```

## Questions?

Feel free to ask questions in:
- [Issues](https://github.com/nadir2609/Smart-Meeting-Notes-Generator/issuess)

Thank you for contributing! 🚀
