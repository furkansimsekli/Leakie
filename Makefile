.PHONY: run

CONFIG = ../.config-files/Leakie/config.py

run: .venv $(CONFIG)
	. .venv/bin/activate && \
	cp $(CONFIG) src && \
	python src/bot.py

.venv: requirements.txt
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt
