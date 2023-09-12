import http.server
import socketserver
import sys

PORT = sys.argv[1] if len(sys.argv) > 1 else 8000


class ExpenseHandler(http.server.BaseHTTPRequestHandler):
    INCOME = 0
    INCOMES_LIST = []
    EXPENSE = 0
    EXPENSE_LIST = []
    SAVINGS = 0
    SAVINGS_LIST = []

    def send_response_html(self, html_content):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content)

    def do_GET(self):
        if self.path == "/":
            self.self.send_response_html(b"<h1>Expense Tracker</h1>")
        elif self.path == "/income":
            self.send_response_html(b"<h1>Income</h1>")
        elif self.path == "/expense":
            self.send_response_html(b"<h1>Expense</h1>")
        elif self.path == "/savings":
            self.send_response_html(b"<h1>Savings</h1>")

    def do_POST(self):
        if self.path == '/submit':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            form_response = b'<html><body><h1>Form submitted</h1><p>' + post_data + b'</p></body></html>'
            self.send_response_html(form_response)
        else:
            self.send_error(404)


socketserver.TCPServer.allow_reuse_address = True

try:
    with http.server.HTTPServer(("", PORT), ExpenseHandler) as httpd:
        print(f"Opening httpd server at port {PORT}")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nShutting down the server.")
