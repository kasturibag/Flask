from api.__init__ import create_app
# from api.config.config import config_dict


app=create_app()

if __name__ == "__main__":
    app.run()