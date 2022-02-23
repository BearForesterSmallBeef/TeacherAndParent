from flask import Blueprint, render_template


main = Blueprint("main", __name__)


@main.route("/teacher/consultations")
def teacher_consultations():
    return render_template("teacher/consultations.html")
