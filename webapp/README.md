## running the server (dev)
```
export FLASK_APP=app.py
flask run
flask db init
flask db migrate
flask db upgrade
```

## running the server (prod)
```
gunicorn --config gunicorn_config.py app:app
```

## s3
[configurar s3cmd](https://docs.digitalocean.com/products/spaces/reference/s3cmd/)
```
s3cmd put images/ s3://maquininha-bucket/images/ --recursive
s3cmd put thumbs/ s3://maquininha-bucket/thumbs/ --recursive
```

### tutoriais usados
[instalar postgresql](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-20-04)

[sqlalchemy](https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/#install-requirements)

