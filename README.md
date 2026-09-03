# Paperquilt website

## Deploy on a Linux host

These steps assume the site will live at `/var/www/paperquilt-website` and Nginx will be the public-facing web server.

1. Install Python 3, Nginx, and Git with the host's package manager.
2. Copy or clone this repository to `/var/www/paperquilt-website` and make `www-data` its owner:

   ```sh
   sudo chown -R www-data:www-data /var/www/paperquilt-website
   ```

3. Create the virtual environment and install the pinned dependencies:

   ```sh
   cd /var/www/paperquilt-website
   sudo -u www-data python3 -m venv .venv
   sudo -u www-data .venv/bin/pip install --upgrade pip
   sudo -u www-data .venv/bin/pip install -r requirements.txt
   ```

4. Install the service and start it:

   ```sh
   sudo cp deploy/paperquilt.service /etc/systemd/system/paperquilt.service
   sudo systemctl daemon-reload
   sudo systemctl enable --now paperquilt.service
   sudo systemctl status paperquilt.service
   ```

5. Copy `deploy/nginx.conf.example` to `/etc/nginx/sites-available/paperquilt`, replace `example.com` with the site's hostname, enable it, and reload Nginx:

   ```sh
   sudo ln -s /etc/nginx/sites-available/paperquilt /etc/nginx/sites-enabled/paperquilt
   sudo nginx -t
   sudo systemctl reload nginx
   ```

6. Add TLS after DNS is pointed at the host, for example with Certbot and its Nginx plugin.

View application logs with `sudo journalctl -u paperquilt.service -f`. Gunicorn is the production WSGI server; Flask's development server is never used by the systemd service.

## Local run

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py
```

The local server listens on `127.0.0.1:5004`. `PORT` and `FLASK_HOST` can override the address, and `FLASK_DEBUG=true` explicitly enables Flask debug mode for local development.

## Generate GitHub Pages files

Render the Flask routes and copy their assets into `github-pages/`:

```sh
python3 staticify.py
```

The output is recreated on every run. The root route becomes `github-pages/index.html`, nested routes become directories containing `index.html`, and the complete `static/` directory is copied alongside them. By default, `CNAME` is generated for `paperquilts.art`; omit it when needed with:

```sh
python3 staticify.py --domain ""
```

The generated directory is the deployable site root. To update the dedicated deployment branch, generate the files on the source branch, copy the contents of `github-pages/` into the root of the `github-pages` branch, and commit the result there.
