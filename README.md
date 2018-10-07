To runserver server use the following procedure:<br />

clone this directory using the following command:

```
$ git clone ssh://git@gitlab.cloud.mobilesdn.org:60022/CES/Policy_Database.git

```
Enter the directory and run the installation file. remember to use "take5" as password where it is inquired except the sudo password.
```
$ cd Policy_Database/src
Policy_Database$ sudo bash installation.sh
(Remember to use take5 as password)
```

Now to RUN the POLICY API follow the following commands:
```
Policy_Database/src$ cd REST_server/
Policy_Database/src/REST_server$ sudo python3 api_server.py
```

Now to run the Django Web Frontend, first navigate to the folder and then run the server. Port specified here is 8000
which can be change but not *) because POLICY API is running on port 80

```
$ cd Policy_Database/src/django_GUI
Policy_Database/src/django_GUI$ python3 manage.py runserver 0.0.0.0:8000
```


Note:
If some locale error occurs while installing django, execute the following commands:
Install all locales when given the option

```
$ export LANGUAGE=en_US.UTF-8
$ export LANG=en_US.UTF-8
$ export LC_ALL=en_US.UTF-8
$ locale-gen en_US.UTF-8
$ sudo dpkg-reconfigure locales
```
