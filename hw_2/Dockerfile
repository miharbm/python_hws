FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-lang-cyrillic \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /HW_2

COPY . .

RUN pip install --no-cache-dir uv

RUN uv sync

CMD ["sh", "-c", "uv run python /app_2_2.py"]