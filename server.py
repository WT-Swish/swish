import rethinkdb as r

from swish.server import app

if __name__ == "__main__":
    r.connect("localhost", 28015).repl()
    app.run(debug=True)
