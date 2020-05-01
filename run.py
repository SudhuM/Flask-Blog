from blog import create_app

app = create_app()
with app.app_context():
    if __name__ == "__main__":
        app.run(debug=True)
