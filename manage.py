from project import create_app
from flask.cli import FlaskGroup

# Config coverage report
app = create_app()
cli = FlaskGroup(app)

if __name__ == '__main__':
     # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    cli()
