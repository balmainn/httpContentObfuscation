imageName=catblog
default: 
	docker build . -t $(imageName)
	docker run -d -p 8000:8000 $(imageName)

build: 
	docker build . -t $(imageName)

run: 
	docker run -d -p 8000:8000 $(imageName)
