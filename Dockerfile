FROM python:3.11.6-alpine3.17

LABEL authors="OleksiyM"

ENV APP /chatbot

ENV POETRY_HOME=$APP/.poetry 

WORKDIR $APP

COPY pyproject.toml $APP/pyproject.toml

COPY poetry.lock $APP/poetry.lock

COPY . .

#COPY . $APP

RUN pip install poetry

#RUN poetry install
RUN poetry config virtualenvs.create false && poetry install --only main

#CMD ["poetry", "shell"]
#ENTRYPOINT ["python", "main.py"]
CMD poetry shell && python main.py
