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

``sudo apt-get install rabbitmq-server``  
``sudo rabbitmqctl add_user admin admin``  
``sudo rabbitmqctl add_vhost ebooking``  
``sudo rabbitmqctl set_permissions -p ebooking admin ".*" ".*" ".*"``  

## Config  
Make a config like sample/config


## Run  
``celery -A tasks.celery_app worker  -l debug -n worker1 -c 10 ``  
``celery -A tasks.celery_app worker  -l debug -n worker2 -Q ORDER -c 1 ``  
``python app.py``  

## API  
**修改酒店上线状态**  
``/api/hotel/cooped/{hotel_id}/online/{is_online}/``  
*is_online* in [0, 1]  
return cooped hotel info  

**添加 RatePlan**
``/api/hotel/{hotel_id}/roomtype/{roomtype_id}/``  
[POST]  


### User
**获取当前登陆用户信息**  
``/api/user/``  
``curl http://BASE_URL/api/user/``  

### Order
**获取当前登陆商户待处理订单数**  
``/api/order/waiting/count/``  
``curl http://BASE_URL/api/order/waiting/count/``  

**获取当前登陆商户的特定订单**  
``/api/order/{order_id}/``  
``curl http://BASE_URL/api/order/1``  
