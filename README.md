# Lambda-Selenium-Chromedriver
Setting up the Selenium,Chromedriver environment in AWS Lambda.   
lambda_function.py contains the process of downloading the file from S3, completing the work through Cellinium in a chrome environment, and uploading the file back to S3.   

---
### 1. Copy lambda_function.py and paste it into your lambda function.
### 2. Do not release the two zip files(chromedriver.zip, selenium.zip) in the layer folder, add them to the lambda layer, respectively, and apply them to the lambda function.
### 3. Check that the test is successful after changing the lambda function to suit your logic.
### 4. If successful, tap Star⭐️ in this repository. Yeah!

https://stackoverflow.com/questions/31329958/how-to-pass-a-querystring-or-route-parameter-to-aws-lambda-from-amazon-api-gatew
event["queryStringParameters"]['queryparam1']

https://velog.io/@sangeun-jo/AWS-lambda%EC%97%90%EC%84%9C-chrome-driver-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0


```
uvicorn main:app --host 0.0.0.0 --port 5000
```

# ssh ec2 연결
```
ssh -i "instagrame-crawl-machine.cer" ubuntu@
ssh -i "instagrame-crawl-machine.cer" ubuntu@ec2-3-39-80-34.ap-northeast-2.compute.amazonaws.com
```

# Ip를 다른 인스턴스에 달았을 경우 변경하는 법
```
https://visu4l.tistory.com/entry/ssh-%EC%9B%90%EA%B2%A9-%EC%A0%91%EC%86%8D-%EC%97%90%EB%9F%ACWARNING-REMOTE-HOST-IDENTIFICATION-HAS-CHANGED
```

# EC2 에 chrome 설치하는 순간
```
https://codediary21.tistory.com/39
```

# FastApi 디버그모드로 실행하는법
```
uvicorn main:app --reload
```

# FastApi 프로덕션 모드로 실행
```
uvicorn main:app --host 0.0.0.0 --port 5000 >> logs.txt 2>&1
```

# SSL https production
```
uvicorn main:app --host 0.0.0.0 --port 5000 --ssl-keyfile=./private.pem --ssl-certfile=./public.pem
uvicorn main:app --host 0.0.0.0 --port 5000 --ssl-keyfile=./key.pem --ssl-certfile=./cert.pem
uvicorn main:app --host 0.0.0.0 --port 5000 --ssl-keyfile=./key.pem --ssl-certfile=./cert.pem
uvicorn main:app --host 0.0.0.0 --port 5000 >> logs.txt 2>&1
uvicorn main:app --host 0.0.0.0 --port 5000
uvicorn main:app --host 0.0.0.0 --port 80 >> logs.txt 2>&1
```

# 파이썬 가상환경 만들기
```
python3 -m venv crawlEnv
```

# 파이썬 가상환경 활성화하기
```
source ./crawlEnv/bin/activate
```

# 파이썬 얼리기
```
pip freeze > requirements.txt
```

# 파이썬 얼린거 설치
```
pip install -r requirements.txt 
```

# 크롬드라이버
https://chromedriver.chromium.org/


# 참고 블로그
https://velog.io/@sangeun-jo/AWS-lambda%EC%97%90%EC%84%9C-chrome-driver-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0


# os.listdir('./Music')

# 디버깅1
https://league-cat.tistory.com/278