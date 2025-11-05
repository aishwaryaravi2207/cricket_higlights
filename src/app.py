from flask import Flask, request, Response
from cricketnews import get_summary_by_match_id

app = Flask(__name__)

@app.route("/get_summary", methods=["GET"])
def get_summary():
    match_id = request.args.get("match_id")
    get_summary_by_match_id(match_id)
    f = open('./article/refined_article.txt','r')
    summary = f.read()
    return Response(summary)

if __name__ == "__main__":
    app.run(debug=True, port=9080)

