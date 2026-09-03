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

## Generate static site

Run the root-level exporter to render the current Flask routes into `/home/runner/work/paperquilt-website/paperquilt-website/github-pages`:

```sh
python3 staticify.py
```

The export includes:

- rendered HTML for each app route
- copied assets under `github-pages/static/`
- `github-pages/CNAME` set to `paperquilts.art`
- `github-pages/.nojekyll`

Optional flags:

```sh
python3 staticify.py --domain paperquilts.art --base-url https://paperquilts.art
```

Pass `--domain ""` to skip writing a `CNAME` file.