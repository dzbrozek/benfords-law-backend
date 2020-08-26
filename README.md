## Benford's law

Simple REST API written in Django/DRF that allows you to verify your dataset against the Benford's law (the first-digit law).
For frontend part visit [benfords-law-frontend](https://github.com/dzbrozek/benfords-law-frontend)


### Running

#### Requirements

This app is using Docker so make sure you have both: [Docker](https://docs.docker.com/install/)
and [Docker Compose](https://docs.docker.com/compose/install/)

#### Bootstrap

To bootstrap the app move to the app directory and call

```
make build
make bootstrap
```

Once it's done the app should be up app and running. You can verify that visiting [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

#### Running

Next time you want to start or stop the the app use `up` or `down` command.

```
make up
```

```
make down
```

#### Users

Test users created during bootstrapping the project.

| Login          | Password | Role  |
|----------------|----------|-------|
| admin          | password | admin |

### Tests

To run the tests use `make test` command
