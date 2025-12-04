# Contributing to CNC Machine Monitor

First off, thank you for considering contributing to CNC Machine Monitor! It's people like you that make this tool better for everyone.

## Code of Conduct

This project and everyone participating in it is expected to maintain a respectful and harassment-free environment.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if applicable**
- **Include your environment details** (OS, Python version, browser)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any examples of similar features in other tools**

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. Ensure your code follows the existing style
4. Update the documentation if needed
5. Write a clear commit message

## Development Setup

1. Clone your fork:
```bash
git clone https://github.com/your-username/cnc-machine-monitor.git
cd cnc-machine-monitor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a branch:
```bash
git checkout -b feature/my-new-feature
```

4. Make your changes and test:
```bash
cd backend
python api.py
```

5. Commit your changes:
```bash
git add .
git commit -m "Add some feature"
```

6. Push to your fork:
```bash
git push origin feature/my-new-feature
```

7. Open a Pull Request

## Style Guidelines

### Python Code

- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small
- Add comments for complex logic

### JavaScript/HTML/CSS

- Use consistent indentation (2 spaces)
- Use meaningful variable and function names
- Add comments for complex sections
- Follow existing code structure

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests when applicable

## Project Structure

```
cnc-machine-monitor/
├── backend/           # Python FastAPI backend
│   ├── api.py        # Main API server
│   └── haas_machine.py  # Machine simulation
├── frontend/          # HTML/JS frontend
│   └── index.html    # Dashboard UI
└── docs/             # Documentation
```

## Testing

Before submitting a PR, ensure:

1. The server starts without errors
2. The dashboard loads correctly
3. Real-time updates work via WebSocket
4. API endpoints return expected data
5. No console errors in browser

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

Thank you for contributing! 🎉
