FROM python
WORKDIR /test_ptoject/
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV ENV=dev
CMD python -m pytest -s --alluredir=test_result/ /test_project/tests/
