from flask import Flask, request, jsonify, redirect, render_template, flash


app = Flask('flask_app')

# Route: ping
@app.route("/")
def ping():
    return 'Forbidden'
