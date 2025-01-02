from swisseat import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host="92.113.145.121", port=80, debug=True)
