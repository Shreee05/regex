from flask import Flask, render_template, request
import re

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/regex-test", methods=["POST"])
def regex_test():
    regex_pattern = request.form.get("regex_pattern")
    test_strings = request.form.get("test_strings").splitlines()

    results = []
    for test_string in test_strings:
        try:
            match = re.search(regex_pattern, test_string.strip())
            if match:
                matched_groups = match.groups()
            else:
                matched_groups = None
            results.append(
                {
                    "test_string": test_string,
                    "match": match,
                    "matched_groups": matched_groups,
                }
            )
        except re.error:
            return "Invalid regular expression"

    return render_template("regex_result.html", results=results)


@app.route("/validate-email", methods=["GET", "POST"])
def validate_email():
    if request.method == "POST":
        email = request.form.get("email")
        is_valid = validate_email_address(email)
        return render_template(
            "email_validation_result.html", email=email, is_valid=is_valid
        )
    return render_template("validate_email.html")


def validate_email_address(email):
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email) is not None


if __name__ == "__main__":
    app.run(port=5000, debug=True)