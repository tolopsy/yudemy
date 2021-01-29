# BACKEND INTENSIVE E-LEARNING PROJECT WITH COURSE SPECIFIC CHAT ROOMS (DJANGO)

This is an e-learning project provisioned as a REST API and a MVT-based platform.

## FEATURES
1. Teachers can create different contents which could be video, files, texts or images
2. Drag and Drop feature to rearrange course contents
3. Chat rooms for every course available for teachers and students
4. Teachers can embed video links from YouTube, Vimeo etc.

## TECHNOLOGIES USED
1. Cache Backend: **Memcached** to cache frequently requested query results
2. **REST API**
3. Communication Store: **Redis**
4. Chat Server: **Asynchronous Server Gateway Interface (ASGI)**
5. WebSocket Handler: **Channels**
6. WebSocket Client using JavaScript to open and maintain client-side connection
7. **JQuery** to interact with DOM
8. Package support to use Redis as channel layer: **channels-redis**
9. Cache monitor: **django-memcache-status**


## Follow the following steps to run this project  on your local machine

```json
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Follow the following steps to configure cache backend (Memcached)

1. Download: Download Memcached from https://memcached.org/downloads

2. Installation:  If you're using Linux, Install Memcached by executing the following command in your shell

   ```json
   ./configure && make && make test && sudo make install
   ```

   If you are using macOS, you can install Memcached with the Homebrew package by executing
   the following command

   ```json
   brew install memcached
   ```

   If you're using Windows, visit https://memcached.org to learn how to install Memcached

3. Launch: Execute the following command after installation to run Memcached

   ```json
   memcached -l 127.0.0.1:11211
   ```
   Now, Memcached should be listening at port 11211

4. Python Binding: The python binding for Memcache (python-memcached) will be installed
   when you ran 'pip install -r requirements.txt'


## Follow the following steps to set up  your channel layer with Redis

1. Installation: For Linux and macOS users, download Redis from https://redis.io/download. 
   Unzip the tar.gz file, change directory to the redis directory and compile Redis with
   the 'make' commmand
   
   For Windows users, enable Windows Subsystem for Linux (WSL), then download and install
   Redis in the Linux system. To learn more on how to do this, click [here](https://redislabs.com/blog/redis-on-windows-10/)

2. Launch: Run the Redis server using the following command in your shell
   ```json
   src/redis-server
   ```
   To use a different port from the default port used by Redis (6379). Specify 
   the port number using the --port flag. Example: src/redis-server --port 6655

3. channels-redis will be installed when you ran 'pip install -r requirements.txt'