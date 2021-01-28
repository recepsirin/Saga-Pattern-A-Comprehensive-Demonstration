from flask import Flask
import yaml

app = Flask(__name__)

config = dict()

with open("config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

app.config['DEBUG'] = config['debug']
app.config['TESTING'] = config['testing']



if __name__ == "__main__":
    app.run(host=config['host'], port=config['port'])
