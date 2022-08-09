from api import app, db
from flask import render_template
from schema import schema
from flask_graphql import GraphQLView

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
