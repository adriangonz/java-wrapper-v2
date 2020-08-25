run:
	python main.py

start-nojava:
	seldon-core-microservice \
		--service-type MODEL \
		NoJava \
		REST

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

start-payloadpassthrough:
	SHOULD_DECODE=false \
	SHOULD_ENCODE=false \
	seldon-core-microservice \
		--service-type MODEL \
		PayloadPassthrough \
		REST

install-dev:
	pip install -r requirements.txt

kill:
	# TODO: JPype seems to leave something hanging that doesn't get killed.
	killall -s 9 seldon-core-microservice
