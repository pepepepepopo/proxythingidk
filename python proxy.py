from flask import Flask, request, jsonify
import urllib.request
import os

app = Flask(__name__)

@app.route("/", methods=["OPTIONS", "POST"])
def proxy():
    if request.method == "OPTIONS":
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response
    
    try:
        data = request.get_json()
        if not data or "url" not in data:
            return jsonify({"error": "Missing 'url' field"}), 400

        url = data["url"]
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            body = response.read().decode('utf-8', errors='replace')
            return jsonify({"status": response.getcode(), "body": body})
    except urllib.error.HTTPError as e:
        return jsonify({"error": "HTTP Error", "code": e.code, "reason": e.reason}), e.code
    except urllib.error.URLError as e:
        return jsonify({"error": "URL Error", "reason": str(e.reason)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
