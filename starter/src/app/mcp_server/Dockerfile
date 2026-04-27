FROM python:3.13-trixie

WORKDIR /app

# Install uv / no venv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin:/app/.local/bin:${PATH}"
ENV UV_SYSTEM_PYTHON=1

# Cache the requirements if possible
COPY src_mcp_server/mcp_calc/* .
RUN uv pip install -r requirements.txt
RUN ls -al

ENTRYPOINT ["python3", "mcp_server.py"]
