from flask import Flask, request, jsonify, redirect, render_template, flash


app = Flask('flask_app')

# Route: ping
@app.route("/ping")
def ping():
    return 'pong'
