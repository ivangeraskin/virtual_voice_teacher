rabbit:
	docker run -d --rm --name voice-rabbit -p 5672:5672 -p 5673:5673  rabbitmq:3

pgadmin:
	docker run --rm -d \
               --name pgadmin \
               -p 8001:80 \
               -e PGADMIN_DEFAULT_EMAIL=test@test.org \
               -e PGADMIN_DEFAULT_PASSWORD=password \
               dpage/pgadmin4:latest

build_tg:
	docker build --tag voice:tg_v0.1 --file ${PWD}/tg/Dockerfile ${PWD}/tg

build_ml:
	docker build --tag voice:ml_v0.1 --file ${PWD}/ml/Dockerfile ${PWD}/ml


build:
	docker build --tag voice:tg_v0.1 --file ${PWD}/tg/Dockerfile ${PWD}/tg
	docker build --tag voice:db_v0.1 --file ${PWD}/db/Dockerfile ${PWD}/db
	docker build --tag voice:ml_v0.1 --file ${PWD}/ml/Dockerfile ${PWD}/ml

run:
	docker-compose up -d rabbit
#	docker-compose up -d postgres
#	docker-compose up -d pgadmin
	docker-compose up -d db
	docker-compose up -d tg
	docker-compose up ml

stop:
	docker-compose down
