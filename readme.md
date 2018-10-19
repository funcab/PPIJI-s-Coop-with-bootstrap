## nginx and uwsgi configuration
1. install nginx: `sudo apt-get install nginx`
2. install uwsgi: pip install uwsgi
3. change the setting.py in django project:
  Debug = False
  Allow_host = ['your id', 'localhost',]
  STATIC_ROOT = os.path.join(BASE_DIR, 'collectedstatic')
  MEDIA_DIR = os.path.join(BASE_DIR, 'media')
  MEDIA_ROOT = MEDIA_DIR
4. Static file migration: python manage.py collectstatic
5. uwsgi configuration in xml way: build a socket.xml under the same filedirection as the manage.py
6. nginx condiguartion: change the server{} in /etc/nginx/nginx.conf 
run the whole project using uwsgi and nginx
1. make sure every port is free to be used: sudo fuser -k 8000/tcp
2. start nginx: nginx -c /etc/nginx/nginx.conf
2.5 after changing the nginx.conf make sure you restart nginx: sudo /etc/init.d/nginx restart
3. start uwsgi: uwsgi --ini mysite.ini
4. run: tail -f uwsgi.log
