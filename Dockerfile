FROM python:3.10-alpine AS base

ARG ENVIRONMENT

ENV PYROOT /pyroot
ENV PYTHONUSERBASE $PYROOT

WORKDIR /usr/src/inventory_app

COPY requirements.txt requirements-dev.txt ./

RUN PIP_USER=1 pip install -U pip

RUN if [ "$ENVIRONMENT" = "production" ]; then \
    PIP_USER=1 pip install -Ur requirements.txt; \
    elif [ "$ENVIRONMENT" = "development" ]; then \
    apk add gcc python3-dev musl-dev linux-headers; \
    PIP_USER=1 pip install -Ur requirements-dev.txt; \
    else \
    echo "Invalid environment"; \
    exit 1; \
    fi

FROM python:3.10-alpine

ENV PYROOT /pyroot
ENV PYTHONUSERBASE $PYROOT
ENV PATH $PYROOT/bin:$PATH

WORKDIR /usr/src/inventory_app

COPY main.py ./
COPY inventory_app ./inventory_app

RUN addgroup -S inventory_app \
    && adduser -S user -G inventory_app -u 1000 \
    && chown -R user:inventory_app /usr/src/inventory_app

COPY --chown=user:inventory_app --from=base ${PYROOT} ${PYROOT}

USER user

EXPOSE 8080

CMD [ "uvicorn", "main:app", "--port", "8080", "--host", "0.0.0.0"]
