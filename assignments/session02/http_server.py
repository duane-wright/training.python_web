import socket
import sys
import mimetypes
import os
import urllib


def response_ok(body, mimetype):

	#print "body: %s" % (body)
	#print "mimetype: %s" % (mimetype)
	
	"""returns a basic HTTP response"""
	resp = []
	resp.append("HTTP/1.1 200 OK")
	#resp.append("Content-Type: text/plain")
	
	str = "Content-Type: "
	str += mimetype
	
	#resp.append("Content-Type: ")
	#resp.append(mimetype)
	
	resp.append(str)
	
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
	
	#print "*********RECEIVED %s" % (uri)
	
	uri_parts = uri.split()
	
	for parts in uri_parts:
		print parts
	
	body = ''
	mimetype = ''
	
	if len(uri_parts) > 1:
		to_match = uri_parts[1]
		
	else:
		to_match = uri_parts[0]
	
	if to_match == '/a_web_page.html': 
		#path = "webroot{0}".format(uri)
		#body = open(path, 'rb').read()
		body = '/a_web_page.html'
		mimetype = 'text/html'
		
	elif to_match == '/make_time.py':
		mimetype = 'text/x-python'
		
	elif to_match == '/':
		body = 'a_web_page.html images make_time.py sample.txt'
		mimetype = 'text/plain'
	
	elif to_match == '/sample.txt':
		mimetype = 'text/plain'
		
	elif to_match == 'JPEG_example.jpg':
		mimetype = 'image/jpeg'
		
	elif to_match == '/images/JPEG_example.jpg':
		mimetype = 'image/jpeg'
		
	elif to_match == 'sample_1.png':
		mimetype = 'image/png'
		
	elif to_match == 'example.com':
		mimetype = response_not_found()
		
	else:
		mimetype = response_not_found()
		
	#print "*********RETURNING %s" % (mimetype)
	
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
                
                # response_ok(body, mimetype)
                
                else:
                    
                    body, ext = resolve_uri(request)
                    
                    #print "*****body: %s" % (body)
                    #print "*****ext: %s" % (ext)
                    
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
