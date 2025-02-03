from flask import Flask, render_template, request
import requests
import time
import threading

app = Flask(__name__)

class CommentBot:
    def __init__(self, tokens, post_id, comments, haters_name, delay):
        self.tokens = tokens
        self.post_id = post_id
        self.comments = comments
        self.haters_name = haters_name
        self.delay = delay

    def start_commenting(self):
        while True:
            try:
                for i, comment in enumerate(self.comments):
                    token = self.tokens[i % len(self.tokens)]
                    url = f"https://graph.facebook.com/v15.0/{self.post_id}/comments"
                    parameters = {'access_token': token, 'message': self.haters_name + ' ' + comment}
                    response = requests.post(url, json=parameters)

                    if response.ok:
                        print(f"[+] COMMENT {i+1} SENT: {self.haters_name} {comment}")
                    else:
                        print(f"[x] FAILED COMMENT {i+1}: {self.haters_name} {comment}")

                    time.sleep(self.delay)
                print("\n[+] ALL COMMENTS SENT, RESTARTING...\n")
            except Exception as e:
                print(f"[!] ERROR: {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        tokens = request.form["tokens"].split("\n")
        post_id = request.form["post_id"]
        comments = request.form["comments"].split("\n")
        haters_name = request.form["haters_name"]
        delay = int(request.form["delay"])

        bot = CommentBot(tokens, post_id, comments, haters_name, delay)
        threading.Thread(target=bot.start_commenting).start()
        
        return "Comment bot started! Check the logs."

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
