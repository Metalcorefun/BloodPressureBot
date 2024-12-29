FROM python:3.13-slim

WORKDIR /blood_pressure_bot

COPY . /blood_pressure_bot
RUN ls -la
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "-u", "run_bot.py"]