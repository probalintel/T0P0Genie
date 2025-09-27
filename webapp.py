#!/usr/bin/env python3
from flask import Flask, render_template, send_from_directory
import os, json

app = Flask(__name__)

OUTPUT_DIR = "output"

@app.route("/")
def index():
    report = ""
    recs = ""
    topo = {}

    # Load report
    report_file = os.path.join(OUTPUT_DIR, "report.txt")
    if os.path.exists(report_file):
        with open(report_file) as f:
            report = f.read()

    # Load recommendations
    rec_file = os.path.join(OUTPUT_DIR, "recommendations.txt")
    if os.path.exists(rec_file):
        with open(rec_file) as f:
            recs = f.read()

    # Load topology.json
    topo_file = os.path.join(OUTPUT_DIR, "topology.json")
    if os.path.exists(topo_file):
        with open(topo_file) as f:
            topo = json.load(f)

    return render_template("index.html",
                           report=report,
                           recs=recs,
                           topo=topo)

@app.route("/topology.png")
def topology_img():
    return send_from_directory(OUTPUT_DIR, "topology.png")

@app.route("/final_report.pdf")
def final_pdf():
    return send_from_directory(OUTPUT_DIR, "final_report.pdf")

if __name__ == "__main__":
    app.run(debug=True, port=5000)

