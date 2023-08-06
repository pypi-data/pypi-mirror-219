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
 
```

## changelogs

- Beta version 1.0.9
- Added Limiter ( from zylo.limiter import Limiter )
- New init app=(__name__)
- Function run() update --> run(host, port, debug)
- JwT updated to vesion --> 1.0.2
- Bug fixed with update --> 1.0.9
- zylo-admin library added, usage will be disclosed soon
- Improved session management


```python

from zylo.limiter import Limiter, render_template

app = Zylo(__name__)
limiter = Limiter(app)

@app.route('/', methods=['GET', 'POST'])
@limiter.limit('10/minutes')
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

```