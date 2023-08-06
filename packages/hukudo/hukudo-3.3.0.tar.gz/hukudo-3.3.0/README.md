# Usage
See [tests/](https://gitlab.com/hukudo/lib/-/tree/main/tests) and
[docs/](https://gitlab.com/hukudo/lib/-/tree/main/1-docs).


# Installation
```
pip install hukudo
```

🔥DRAFT🔥 For Gitlab Tools
```
pip install hukudo[gitlab]
```


# Testing
Install https://gitlab.com/hukudo/ingress/-/tags/2022-05.3 or later

Start services
```
docker-compose up -d --build --remove-orphans
```

Create grafana API key:

- https://grafana.dev.0-main.de/org/apikeys login with `admin` / `test`
- https://grafana.dev.0-main.de/org/apikeys > New
   - name: test
   - role: admin
   - Add

Configure the test environment:
```
export GRAFANA_URL=https://grafana.dev.0-main.de/
export GRAFANA_API_KEY=eyJrIjoiaG8zZEE5N1pmUUVBc3lHRElvT1lnOWNhYkd3ck9JNGIiLCJuIjoidGVzdCIsImlkIjoxfQ==
export GRAFANA_CLIENT_ROOT_CA=$HOME/ingress/root.crt
```

```
make
```


# Development
See [1-docs/development.md]
