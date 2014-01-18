import socket
import sys
import mimetypes
import os
import urllib


def response_ok(body, mimetype):
    """returns a basic HTTP response"""
    resp = []
    resp.append("HTTP/1.1 200 OK")
    resp.append("Content-Type: text/plain")
    resp.append("")
    resp.append("this is a pretty minimal response")
    return ("\r\n".join(resp), body, mimetype)


def response_method_not_allowed():
    """returns a 405 Method Not Allowed response"""
    resp = []
    resp.append("HTTP/1.1 405 Method Not Allowed")
    resp.append("")
    return "\r\n".join(resp)
    
    
def response_not_found():
    """returns a 404 Response Not Found response"""
    resp = []
    resp.append("HTTP/1.1 404 Response Not Found")
    resp.append("")
    return "\r\n".join(resp)


def parse_request(request):
    first_line = request.split("\r\n", 1)[0]
    """here is the uri"""
    method, uri, protocol = first_line.split()  
    if method != "GET":
        raise NotImplementedError("We only accept GET")
    print >>sys.stderr, 'request is okay'
    return uri


def resolve_uri(uri):
	
	dirlist = []
	
	mimetype = ""
	
	filecont = ""
	
	if os.path.isdir(uri):
	
		dirlist = os.listdir(uri)
		
		mimetype = "text/plain"
		
		return (dirlist, mimetype)
	
	elif os.path.isfile(uri):
	
		filecont = uri.read()
		
		url = urllib.pathname2url(uri)
		
		mimetype = mimetypes.guess_type(url)
		
		return (filecont, mimetype)
		
	else:
	
		response_not_found()


def server():
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print >>sys.stderr, "making a server on %s:%s" % address
    sock.bind(address)
    sock.listen(1)
    
    try:
        while True:
            print >>sys.stderr, 'waiting for a connection'
            conn, addr = sock.accept() # blocking
            try:
                print >>sys.stderr, 'connection - %s:%s' % addr
                request = ""
                while True:
                    data = conn.recv(1024)
                    request += data
                    if len(data) < 1024 or not data:
                        break

                try:
                    parse_request(request)
                    
                except NotImplementedError:
                    response = response_method_not_allowed()
                
                # response_ok(body, mimetype)
                
                else:
                    
                    body, ext = resolve_uri(request)
                    
                    response = response_ok(body, ext)

                print >>sys.stderr, 'sending response'
                conn.sendall(response)
            finally:
                conn.close()
            
    except KeyboardInterrupt:
        sock.close()
        return


if __name__ == '__main__':
    server()
    sys.exit(0)
