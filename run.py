from server import createapp

app = createapp(debug = False)

if __name__ == "__main__":
    app.run()