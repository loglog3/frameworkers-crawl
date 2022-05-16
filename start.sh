#
cd /home/ubuntu/seungmin/frameworkers-crawl
#
git pull
#
pip3 install -r requirements.txt 
#
#
source ./crawlEnv/bin/activate
#
uvicorn main:app --host 0.0.0.0 --port 5000