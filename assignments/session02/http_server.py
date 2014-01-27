import socket
import sys
import mimetypes
import os
import urllib


def response_ok(body, mimetype):

	"""returns a basic HTTP response"""
	resp = []
	resp.append("HTTP/1.1 200 OK")
	#resp.append("Content-Type: text/plain")
	resp.append("Content-Type: {}".format(mimetype))
	resp.append("")
	#resp.append("this is a pretty minimal response")
	resp.append(body)
	return "\r\n".join(resp)
	
	
def response_method_not_allowed():
    """returns a 405 Method Not Allowed response"""
    resp = []
    resp.append("HTTP/1.1 405 Method Not Allowed")
    resp.append("")
    return "\r\n".join(resp)
    
    
def response_not_found():
    """returns a 404 Response Not Found response"""
    resp = []
    resp.append('HTTP/1.1 404 Not Found')
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
	
	body = ''
	mimetype = ''
	
	path = ''

	# if uri is a directory		
	if '.' not in uri:
		path = "webroot" + uri
		if os.path.exists(path):
			body = os.listdir(path)
			mimetype = 'text/plain'
		else:
			raise ValueError(404)
			response_not_found()
	# if uri is an image file
	elif uri[-3:] == "jpg" or uri[-3:] == "png":
		path = "webroot/images/" + uri
		if os.path.exists(path):
			body = open(uri, 'rb').read()
			mimetype = mimetypes.guess_type(uri)
		else:
			raise ValueError(404)
			response_not_found()
	# if uri is a non-image file	
	elif '.' in uri:
		path = "webroot" + uri
		if os.path.exists(path):
			body = open(path, 'rb').read()
			mimetype = mimetypes.guess_type(uri)[0]
		else:
			raise ValueError(404)
			response_not_found()	
	else:
		raise ValueError(404)
		response_not_found()
		
	return (body, mimetype)
	

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
                
                else:
                    
                    body, mimetype = resolve_uri(parse_request(request))
                    
                    response = response_ok(body, mimetype)

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
