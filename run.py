from flask import Flask, render_template, request
from api.alerts import alerts_bp
from storage.alerts import get_alerts, get_dashboard_summary

app = Flask(__name__)

app.register_blueprint(alerts_bp, url_prefix="/api")

@app.route("/")
def dashboard_page():
    summary = get_dashboard_summary()
    return render_template("dashboard.html", summary=summary)

@app.route("/alerts")
def alerts_page():
    severity_filter = request.args.get("severity", "ALL")
    alerts = get_alerts()

    if severity_filter != "ALL":
        alerts = [alert for alert in alerts if alert["severity"] == severity_filter]

    return render_template(
        "alerts.html",
        alerts=alerts,
        selected_severity=severity_filter
    )

@app.route("/logs")
def logs_page():
    alerts = get_alerts()
    return render_template("logs.html", alerts=alerts)

if __name__ == "__main__":
    app.run(debug=True)