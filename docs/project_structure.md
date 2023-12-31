## Project structure:
The project is organized as a mono repository. In the main folder, you'll find essential configurations for linters, formatters, gitignore, and license, along with a readme file. Docker-compose.yml files and their configurations should be stored in the /docker directory. For support documentation, use the /docs folder, and make sure to include links to these files in the main readme file. Keep all applications in the backend/apps folder. Each application should have its own folder with Poetry configs and its virtual environment. Common scripts should be placed in the /scripts folder. The project structure example is illustrated below:

## Code style
The code must adhere to the guidelines outlined in [PEP 8 – Style Guide for Python Code](peps.python.org). Ensure that the line length does not exceed 80 characters. Additionally, the code should be fully typed, with exceptions allowed only when a third-party library lacks a stub file.
