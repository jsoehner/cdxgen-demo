# Contributing to cdxgen-demo

Thank you for your interest in contributing to cdxgen-demo! This project provides a demonstration of the cdxgen tool for generating Software Bill of Materials (SBOMs).

## Code of Conduct
Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs
1. **Check existing issues** - Search the issue tracker to see if the bug has already been reported.
2. **Create a new issue** - If not found, create a new issue using the bug report template.
3. **Provide details** - Include:
   - Version of cdxgen-demo
   - Operating system
   - Steps to reproduce
   - Expected vs actual behavior
   - Relevant logs or screenshots

### Suggesting Features
1. **Check existing requests** - Search issues for similar feature requests.
2. **Create a feature request** - Use the feature request template.
3. **Describe the use case** - Explain why this feature would be valuable to the users.

### Contributing Code
1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Run tests**: Ensure all tests pass before submitting.
5. **Commit your changes** with a descriptive message following Conventional Commits.
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Create a Pull Request**

## Development Setup

### Prerequisites
- Python 3.x
- Pip

### Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/jsoehner/cdxgen-demo.git
   cd cdxgen-demo
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run Tests**:
   - Execute the project's test suite to ensure your changes don't introduce regressions.

## Commit Message Guidelines
We use **Conventional Commits**. Please use the following prefixes:
- `feat:` A new feature
- `fix:` A bug fix
- `docs:` Documentation only changes
- `refactor:` A code change that neither fixes a bug nor adds a feature
- `perf:` A code change that improves performance
- `test:` Adding missing tests or correcting existing tests
- `chore:` Changes to the build process or auxiliary tools and libraries

Example: `feat(demo): add new example for SBOM generation`

## Pull Request Process
1. Ensure all tests pass.
2. Update documentation (if applicable).
3. Add tests for new functionality.
4. Fill out the PR template completely.
5. Request review from maintainers.

## Questions?
Feel free to open an issue for questions or join discussions in existing issues.
