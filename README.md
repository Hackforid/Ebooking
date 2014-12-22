# EBooking

## 部署
**依赖：**  
python2.7  
python-dev  
MySQL  
rabbitmq-server  

**Install**  
1.Python lib  
``sudo pip install -r requirements.txt``  

2.Step Celery  
as http://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html#broker-rabbitmq  

``sudo pip install rabbitmq-server``  
``sudo rabbitmqctl add_user admin admin``  
``sudo rabbitmqctl add_vhost ebooking``  
``sudo rabbitmqctl set_permissions -p ebooking admin ".*" ".*" ".*"``  


##Run  
``celery -A tasks.celery_app worker  -l debug -n worker1``  
``celery -A tasks.celery_app worker  -l debug -n worker2 -Q ORDER``  
``python app.py``  


