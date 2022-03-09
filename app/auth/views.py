from flask import Blueprint, redirect, render_template

from .forms import RegisterTypeForm, RegisterParentForm, RegisterTeacherForm

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["GET", 'POST'])
def signup_user_status():
    register_form = RegisterTypeForm()
    if register_form.validate_on_submit():
        user_status = register_form.user_status.data
        return redirect(f"/signup/{user_status}")
    return render_template("auth/register.html", form=register_form,
                           header="Регистрация. Тип пользователя.")


@auth.route("/signup/parent", methods=["GET", "POST"])
def register_parent():
    register_form = RegisterParentForm()
    if register_form.validate_on_submit():
        return redirect("/login")
    return render_template("auth/register.html", form=register_form,
                           header="Регистрация. Родитель.")


@auth.route("/signup/teacher", methods=["GET", "POST"])
def register_teacher():
    register_form = RegisterTeacherForm()
    if register_form.validate_on_submit():
        return redirect("/login")
    return render_template("auth/register.html", form=register_form,
                           header="Регистрация. Учитель.")
