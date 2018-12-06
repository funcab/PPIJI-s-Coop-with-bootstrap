## virtualenv and django configuration
1. install virtualenv：
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --force-reinstall
pip3 install virtualenv
pip3 install virtualenvwrapper
```
2. start virtualenv:
```
source virtualenvwrapper.sh
mkvirtualenv rango
workon rango
```
3. install django:`pip3 install -U django==1.9.10` 
## nginx and uwsgi configuration
1. install nginx: `sudo apt-get install nginx`
2. install uwsgi: `pip3 install uwsgi`
3. change the setting.py in django project:
  ```
  Debug = False
  Allow_host = ['your id', 'localhost',]
  STATIC_ROOT = os.path.join(BASE_DIR, 'collectedstatic')
  MEDIA_DIR = os.path.join(BASE_DIR, 'media')
  MEDIA_ROOT = MEDIA_DIR
  ```
4. Static file migration: `python manage.py collectstatic`
5. uwsgi configuration in ini way: build a mysite.ini under the same filedirection as the manage.py
6. nginx condiguartion: change the server{} in `/etc/nginx/nginx.conf ` `/etc/nginx/sites-enabled/default `
## run the whole project using uwsgi and nginx
1. start virtualenv:
```
source virtualenvwrapper.sh
workon rango
```
2. make sure every port is free to be used: `sudo fuser -k 8000/tcp`
3. start nginx & after changing the nginx.conf make sure you restart nginx: `sudo /etc/init.d/nginx restart`
4. start uwsgi:`uwsgi --ini mysite.ini`
5. run: `tail -f uwsgi.log`
## After updating ubuntu and Python...
1. 检查新版本的python路径是否加入PYTHONPATH:
 ```
 $ echo $PYTHONPATH
 ```
 如果没有反应，需要找到Python安装目录下的site-packages目录把它添加到PYTHONPATH：  
  - 找到site-packages目录：
  ```
  $ python
Python 2.7.5 (v2.7.5:ab05e7dd2788, May 13 2013, 13:18:45)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import site
>>> print(site.getsitepackages()[0])
'/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages' #site-package目录
>>> quit()
  ```
  - 将它添加到配置中。打开.bashrc
 ```
 $ vim .bashrc
 ```
 - 把下述代码添加到.bashrc末尾：
  ```
  export PYTHONPATH=$PYTHONPATH:<PATH_TO_SITE-PACKAGES>  
  ```
2. 重装pillow
3. 重新安装virtualenv，见开头
4. 重启virtualenv，见开头（重建rango除外）
5. 重装Django，nginx，uwsgi
6. 重装web应用里用到的包：
```
  $ pip3 install pymysql  
  $ pip3 install -U django-registration-redux==1.4   
  $ pip3 install django-bootstrap-toolkit  
 ```
7. 防止还有遗漏的包，先进入虚拟环境，在无uwsgi和nginx的环境下在项目根目录下运行：  
  ```
  $ python3 manage.py runserver 0.0.0.0:8000
  ```
8. 无误后，进入虚拟环境，启动uwsgi和nginx。
