from flask import Flask, request, render_template
from app.model import *

from app import app


if __name__ == "__main__":
	app.run(port=5001, debug=True)