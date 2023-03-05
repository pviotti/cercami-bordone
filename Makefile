.PHONY: docker-build docker-run docker-push deploy clean

# TODO target to sync transcription folder

build: npm-build docker-build

docker-build:
	docker build -t pviotti/cercamibordone .

docker-run:
	docker run -p 8000:5000 -v ./output/transcriptions:/app/transcriptions pviotti/cercamibordone

docker-push:
	docker push pviotti/cercamibordone:latest

deploy:
	ssh vshed.xyz "cd apps; docker-compose pull cercamibordone; docker-compose rm -sf cercamibordone; docker-compose up -d cercamibordone; docker-compose ps"

npm-build:
	cd frontend; npm run build

sync-transcr:
	rsync -avu output/transcriptions/ vshed.xyz:~/apps/data/cercamibordone

# check if there are episodes with the same date
check-duplicates:
	ls output/episodes-original/ | cut -d"_" -f1 | sort | uniq -c | sort -n
