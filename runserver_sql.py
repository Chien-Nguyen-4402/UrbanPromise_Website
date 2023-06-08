import sys
import copy_app as app

PORT = 5000
def main():


   if len(sys.argv) != 1:
       print('Usage: ' + sys.argv[0], file=sys.stderr)
       sys.exit(2)


#    try:
#     #    port = int(sys.argv[1])
    
#    except Exception:
#        print('Port must be an integer.', file=sys.stderr)
#        sys.exit(2)

   try:
        app.app.run(host='0.0.0.0', port=PORT,
            ssl_context=('cert.pem', 'key.pem'),threaded = True)
   except Exception as ex:
       print(ex, file=sys.stderr)
       sys.exit(1)


if __name__ == '__main__':
   main()
