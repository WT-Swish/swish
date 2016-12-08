import rethinkdb as r

import config
from swish.server import app

if __name__ == "__main__":
    r.connect("localhost", 28015).repl()
    app.run(config.BASE, config.PORT, debug=True)
