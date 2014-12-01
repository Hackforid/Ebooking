# IceFrog
## API
所有API基于**RESTful**设计  
请设置``content_type``为 ``application/json``  
参数为json格式，置于content_body中  

response为标准Betterwood json格式  
``{errcode: 0, errmsg: '', result: T}``
 

**通过provider_id添加Hotel**

``
api/privider/{provider_id}/
``

*POST:*  
    {hotel_id: {1, 2, 3}}  
    

**通过provider_id删除Hotel**
``api/provider/{provider_id}/``

*DELETE:*
    request: {hotel_id: {1, 2, 3}}
    response: {errcode: 0}

**查询Hotel**
``api/provider/{provider_id}/hotel/``

*GET:*
    request: {hotel_id: {1, 2, 3}}
    response: {errcode: 0, errmsg: '', result: undefine}
    
**查询RoomType**    
``api/provider/{provider_id}/hotel/{hotel_id}/roomtype/``

*GET:**
    request: {roomtype_id: {1, 2, 3}}
    response: {errcode: 0, errmsg: '', result: undefine}

## SQL design 
username: root  
password: root  
host:     192.168.10.15  
database: ebooking-admin  

