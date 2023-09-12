import http.server
import json
import socketserver
import sys
from trackers import IncomeManager
from trackers import ExpenseManager
from trackers import SavingsManager

PORT = sys.argv[1] if len(sys.argv) > 1 else 8000


class ExpenseHandler(http.server.BaseHTTPRequestHandler):
    income_manager = IncomeManager()
    expense_manager = ExpenseManager()
    savings_manager = SavingsManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def send_response_html(self, html_content):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content)

    def render_home(self):
        with open("ejercicio17/tracker_home.html", "rb") as f:
            html_content = f.read().decode('utf-8')
            html_content = html_content.replace("{{income}}", f"${self.income_manager.get_income():.2f}")
            html_content = html_content.replace("{{expense}}", f"${self.expense_manager.get_expense():.2f}")
            html_content = html_content.replace("{{savings}}", f"${self.savings_manager.get_saving():.2f}")
            self.send_response_html(html_content.encode())

    def do_GET(self):
        if self.path == "/":
            with open("ejercicio17/tracker_home.html", "rb") as f:
                html_content = f.read().decode('utf-8')
                html_content = html_content.replace("{{income}}", f"${self.income_manager.get_income():.2f}")
                html_content = html_content.replace("{{expense}}", f"${self.expense_manager.get_expense():.2f}")
                html_content = html_content.replace("{{savings}}", f"${self.savings_manager.get_saving():.2f}")
                self.send_response_html(html_content.encode())

        elif self.path == "/income":
            with open("ejercicio17/income_tracker.html", "rb") as f:
                self.send_response_html(f.read())

        elif self.path == "/expense":
            with open("ejercicio17/expense_tracker.html", "rb") as f:
                self.send_response_html(f.read())

        elif self.path == "/savings":
            with open("ejercicio17/savings_tracker.html", "rb") as f:
                self.send_response_html(f.read())

        else:
            self.send_error(404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_data = json.loads(post_data)

        if self.path == "/income":
            self.income_manager.add_income(post_data['income'])
            self.send_response(200)
            self.render_home()

        elif self.path == "/expense":
            self.expense_manager.add_expense(post_data['expense'])
            self.send_response(200)
            self.render_home()

        elif self.path == "/savings":
            self.savings_manager.add_saving(post_data['savings'])
            self.send_response(200)
            self.render_home()

        else:
            self.send_error(404)


socketserver.TCPServer.allow_reuse_address = True


try:
    with http.server.HTTPServer(("", PORT), ExpenseHandler) as httpd:
        print(f"Opening httpd server at port {PORT}")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nShutting down the server.")
