from app import create_app, db, models

app = create_app()

@app.shell_context_processor
def get_context():
    return dict(app=app, db=db, models=models)


if __name__ == "__main__":
    app.run(debug=True)