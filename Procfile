web: sed "s#^\(  url:\) \(.*\)#\1 $DATABASE_URL#g" config/prod/app.yml; blueberrypy serve -b 0.0.0.0:$PORT -e production -P /tmp/douhack.pid
