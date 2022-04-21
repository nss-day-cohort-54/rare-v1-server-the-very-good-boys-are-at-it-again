from http.server import BaseHTTPRequestHandler, HTTPServer
import json


from views import get_all_posts, get_single_post, create_post, delete_post, update_post

from views.user import create_user, login_user
from views import get_all_categories, get_single_category, create_category, delete_category, update_category
from views.user_requests import get_all_users, get_single_user
from views import get_all_comments, get_single_comment, delete_comment, update_comment, create_comment
from views import get_all_tags, update_tag, delete_tag,create_tag
from views import get_all_reactions
from views import get_all_subscriptions, get_single_subscription, delete_subscription, create_subscription
from views import get_all_demotion_queues, get_single_demotion_queue, delete_demotion_queue, create_demotion_queue



class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self):
        """Parse the url into the resource and id"""
        path_params = self.path.split('/')
        resource = path_params[1]
        if '?' in resource:
            param = resource.split('?')[1]
            resource = resource.split('?')[0]
            pair = param.split('=')
            key = pair[0]
            value = pair[1]
            return (resource, key, value)
        else:
            id = None
            try:
                id = int(path_params[2])
            except (IndexError, ValueError):
                pass
            return (resource, id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                        'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                        'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        
        """Makes a get request to the server """
        self._set_headers(200)
        response = {}
        parsed = self.parse_url()
        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "posts":
                if id is not None:
                    response = f"{get_single_post(id)}"
                else:
                    response = f"{get_all_posts()}"
            if resource == "users":
                if id is not None:
                    response = f"{get_single_user(id)}"
                else:
                    response = f"{get_all_users()}"

            if resource == "tags":
                response = f"{get_all_tags()}"
            if resource == "reactions":
                response = f"{get_all_reactions()}"
            if resource == "categories":
                if id is not None:
                    response = f"{get_single_category(id)}"
                else:
                    response = f"{get_all_categories()}"

            if resource == "comments":
                if id is not None:
                    response = f"{get_single_comment(id)}"
                else:
                    response = f"{get_all_comments()}"
            
            if resource == "subscriptions":
                if id is not None:
                    response = f"{get_single_subscription(id)}"
                else:
                    response = f"{get_all_subscriptions()}"

            if resource == "demotionqueue":
                if id is not None:
                    response = f"{get_single_demotion_queue(id)}"
                else:
                    response = f"{get_all_demotion_queues()}"


        self.wfile.write(f"{response}".encode())

    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len))
        response = ''
        resource, _ = self.parse_url()

        new_post = None

        new_tag = None

        if resource == 'login':
            response = login_user(post_body)
        if resource == 'register':
            response = create_user(post_body)
        if resource == 'posts':
            new_post = create_post(post_body)
            self.wfile.write(f"{new_post}".encode())
        if resource == 'tags':
            new_tag = create_tag(post_body)
            self.wfile.write(f"{new_tag}".encode())
        if resource == 'categories':
            response = create_category(post_body)  
        if resource == 'comments':
            new_comment = create_comment(post_body)
            self.wfile.write(f"{new_comment}".encode())
        if resource == 'subscriptions':
            new_subscription = create_subscription(post_body)
            self.wfile.write(f"{new_subscription}".encode())
        if resource == 'demotionqueue':
            new_demotion_queue = create_demotion_queue(post_body)
            self.wfile.write(f"{new_demotion_queue}".encode())



        self.wfile.write(response.encode())

    def do_PUT(self):
        """Handles PUT requests to the server"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url()

        success = False

        if resource == "tags":
            success = update_tag(id, post_body)
        if resource == "posts":
            success = update_post(id, post_body)
        if resource == "comments":
            success = update_comment(id, post_body)
        if resource == "categories":
            success = update_category(id, post_body)    
        # rest of the elif's
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        """Handle DELETE Requests"""
        self._set_headers(204)
        # Parse the URL
        (resource, id) = self.parse_url()#possibly needs self.path param

        if resource == "posts":
            delete_post(id)
        if resource == "tags":
            delete_tag(id)
        if resource == "comments":
            delete_comment(id)
<<<<<<< HEAD
        if resource == "subscriptions":
            delete_subscription(id)
        if resource == "demotionqueue":
            delete_demotion_queue(id)
=======
        if resource == "categories":
            delete_category(id)    
>>>>>>> main
        self.wfile.write("".encode())

def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
