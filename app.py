
from website import create_app


app = create_app()


if __name__ == "__main__": #used so that when we import this file to other file it does not run website again
    app.run(debug=False,host='0.0.0.0')