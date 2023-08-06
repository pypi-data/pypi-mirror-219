# Zylo

Zylo is a lightweight web framework made with love.

## Features

- Simple and intuitive routing
- Template rendering using Jinja2
- Session management with the sessions library
- Static file serving

## Installation

You can install Zylo using pip:


```bash
pip install zylo

```

## Usage

```python
from zylo import Zylo

app = Zylo()

@app.route('/')
def home(request):
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
