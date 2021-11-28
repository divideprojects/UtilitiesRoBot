test:
	@pre-commit run --all-files

run:
	@python3 -m minibots

clean:
	@pyclean .
	@rm -rf minibots/*.session minibots/*.session-journal
