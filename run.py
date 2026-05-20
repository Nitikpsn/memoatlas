from app import create_app

app = create_app()

if __name__ == "__main__":
    # debug=True lets the server restart automatically when you change code
    app.run(debug=True)