# Tkinter MVC App

![CI](https://github.com/DiasPedroQA/tkinter-mvc-app/actions/workflows/ci-cd.yml/badge.svg)
![Coverage](https://codecov.io/gh/DiasPedroQA/tkinter-mvc-app/branch/main/graph/badge.svg)

## Overview

Tkinter MVC App is a Python desktop application structured with the Model-View-Controller (MVC) design pattern.
Its goal is to offer a clean architecture for batch file processing and GUI interaction using Tkinter.

## Preview

![Interface Screenshot](docs/screenshot.png) <!-- Altere o caminho ou remova se ainda não tiver a imagem -->

## Project Structure

```plaintext
tkinter-mvc-app
├── src
│   ├── controllers          # Application controllers
│   ├── models               # Data models
│   ├── views                # User interface views
│   ├── tools                # Utility functions
│   └── app.py               # Entry point of the application
├── tests                    # Unit tests
├── .github/workflows        # CI/CD configuration
├── requirements.txt         # Dependencies
├── README.md                # Documentation
├── setup.py                 # Packaging (optional)
└── Makefile                 # Dev utility commands
````

## Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/DiasPedroQA/tkinter-mvc-app.git
cd tkinter-mvc-app
pip install -r requirements.txt
```

## Usage

To run the application:

```bash
python src/app.py
```

## Useful Makefile Commands

You can also use the Makefile for common tasks:

```bash
make install      # Install dependencies
make test         # Run tests
make run          # Start the application
make lint         # Lint with Black, isort, flake8
make mypy         # Static typing check
make coverage     # Test coverage report
make clean        # Remove temp files
make format       # Auto-format code
make security     # Run Bandit security check
make update-deps  # Update Python dependencies
```

## Testing

Run the test suite with:

```bash
pytest
```

Or via Makefile:

```bash
make test
```

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration.
The pipeline (`.github/workflows/ci-cd.yml`) automatically installs dependencies and runs tests on push and pull requests to the `main` branch.

Dependabot is also configured to keep GitHub Actions and Python dependencies up to date.

## Contributing

Contributions are welcome! To contribute:

1. Fork this repository
2. Create a branch: `git checkout -b feature/nova-funcionalidade`
3. Commit your changes: `git commit -m "feat: nova funcionalidade"`
4. Push to your fork: `git push origin feature/nova-funcionalidade`
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
