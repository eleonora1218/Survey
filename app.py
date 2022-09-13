from flask import Flask, request, render_template, redirect, flash, session
# from surveys import satisfaction_survey, personality_quiz
from surveys import satisfaction_survey as survey
from flask_debugtoolbar import DebugToolbarExtension

# key names will use to store some things in the session;
# put here as constants so we're guaranteed to be consistent in
# our spelling of these
RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "123-ABC-987-WALDO"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 

debug = DebugToolbarExtension(app)

# http://127.0.0.1:5000/
@app.route("/")
def show_survey_start():
    """Select a survey."""
    return render_template("survey_start.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question."""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question, survey=survey)


@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""
    return render_template("completion.html", survey=survey)