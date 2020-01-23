# API

## Requisitos
Configurar o banco de dados
    * As configurações do arquivo `docker-compose` devem ser ajustadas de acordo com as configurações do seu banco de dados
    * O banco de dados deverá ter o schema "CARONAFGA" criado devidamente de acordo com o arquivo create.sql

## Colocando no ar

Com o Docker e Docker-Compose instalados, basta apenas utilizar os comandos:

```shell
    sudo docker-compose up
```
## Comandos uteis
Caso esteja tendo problema a se conectar no banco de dados local a partir do container, utilize os comandos:

```sql
CREATE USER 'admin'@'host_docker' IDENTIFIED BY '0000';
GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER,INDEX on CARONAFGA.* TO 'admin'@'host_docker' IDENTIFIED BY '0000';
flush privileges;
```

