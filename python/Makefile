run:
	python main.py

start-baseline:
	seldon-core-microservice \
		--service-type MODEL \
		Baseline \
		REST

start-protobufencoding:
	seldon-core-microservice \
		--service-type MODEL \
		ProtobufEncoding \
		REST

install-dev:
	pip install -r requirements.txt

kill:
	# TODO: JPype seems to leave something hanging that doesn't get killed.
	killall -s 9 seldon-core-microservice
