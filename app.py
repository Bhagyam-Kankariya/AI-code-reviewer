
from flask import Flask, render_template, request
import os

app = Flask(__name__)

USE_MOCK_MODE = True   # 🔥 CHANGE TO False WHEN YOU ADD BILLING

@app.route("/", methods=["GET", "POST"])
def index():
    review = ""

    if request.method == "POST":
        code = request.form["code"]
        language = request.form["language"]

        if USE_MOCK_MODE:
            review = f"""
✅ MOCK AI CODE REVIEW (No API Used)

📌 Language: {language}

🔹 Explanation:
This code performs a basic operation. It defines logic and executes it step by step.

⚠️ Issues Found:
- Possible logical or runtime error
- Missing input validation
- Code readability can be improved

✅ Suggested Improvements:
- Add proper parameters
- Use meaningful variable names
- Handle edge cases

⭐ Optimized Version Example:
(Add comments, validation, and error handling)

📊 Code Quality Score: 72 / 100
"""
        else:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            prompt = f"""
You are an expert programming tutor.

Review the following {language} code:
1. Explain what the code does
2. Identify errors
3. Suggest improvements
4. Provide optimized version
5. Give a score out of 100

Code:
{code}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            review = response.choices[0].message.content

    return render_template("index.html", review=review)

if __name__ == "__main__":
    app.run(debug=True)
