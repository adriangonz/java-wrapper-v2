install-dev:
	GO111MODULE=on go get github.com/bojand/ghz/cmd/ghz@v0.55.0
	GO111MODULE=on go get github.com/rakyll/hey@v0.1.3

generate:
	python generator.py

benchmark-rest:
	hey \
		-n 10000 \
		-c 100 \
		-m POST \
		-T 'application/json' \
		-D ./data/rest-requests.json \
		http://localhost:5000/api/v1.0/predictions

