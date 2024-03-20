# Описание
Изменения коснулись конечной точки с которой стягиваем данные и json структуры. Также добавилось несколько параметров, которые необходимы для работы. \
Вот все параметры, которые необходимы в файле `.env`:
- `PROXY_HOST `
- `PROXY_PORT` 
- `PROXY_LOGIN` 
- `PROXY_PASSWORD` 
- `TWITTER_AUTH_TOKEN` 
- `TWITTER_CT0_TOKEN`
- `TWITTER_BEARER_TOKEN` \
\
`TWITTER_AUTH_TOKEN` и `TWITTER_CT0_TOKEN` берутся из cookies (`auth_token` и `ct0` соответственно) \
`TWITTER_BEARER_TOKEN` необходимо достать, например, из `client_event.json` (в разделе `Request Headers` пункт `Authorization` - скопировать все после `Bearer`) \
\
Не уверен насколько данное решение вас устроит, так как я все же обращаюсь к API твиттера, хотя и не совсем так, как предполагается документацией, наверное