test:
	@pre-commit run --all-files

run:
	@python3 -m bots

clean:
	@pyclean .