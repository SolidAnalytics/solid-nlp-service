```docker-compose up --build```

```curl -u guest:guest -X POST -H "Content-Type: application/json" -d '{"properties":{},"routing_key":"input_queue","payload":"[\"101\", \"Эппл отвратные пидарасы просто нажрались хуев айфон хуета собачья\", \"Apple\"]","payload_encoding":"string"}' http://localhost:15672/api/exchanges/%2f/amq.default/publish```

```curl -u guest:guest -X POST -H "Content-Type: application/json" -d '{"properties":{},"routing_key":"input_queue","payload":"[\"102\", \"Google анонсировала новую версию Android.\", \"Google\"]","payload_encoding":"string"}' http://localhost:15672/api/exchanges/%2f/amq.default/publish```

```curl -u guest:guest -X POST -H "Content-Type: application/json" -d '{"properties":{},"routing_key":"input_queue","payload":"[\"103\", \"Microsoft заключила выгодный контракт с крупной компанией.\", \"Microsoft\"]","payload_encoding":"string"}' http://localhost:15672/api/exchanges/%2f/amq.default/publish```

```curl -u guest:guest -X POST -H "Content-Type: application/json" -d '{"properties":{},"routing_key":"input_queue","payload":"[\"104\", \"Tesla запустила новую модель электрокара.\", \"Tesla\"]","payload_encoding":"string"}' http://localhost:15672/api/exchanges/%2f/amq.default/publish```

```curl -u guest:guest -X POST -H "Content-Type: application/json" -d '{"properties":{},"routing_key":"input_queue","payload":"[\"105\", \"Amazon увеличила штат разработчиков.\", \"Amazon\"]","payload_encoding":"string"}' http://localhost:15672/api/exchanges/%2f/amq.default/publish```

```curl -u guest:guest -X POST -H "Content-Type: application/json" -d '{"properties":{},"routing_key":"input_queue","payload":"[\"106\", \"Meta получила рекордную выручку за квартал.\", \"Meta\"]","payload_encoding":"string"}' http://localhost:15672/api/exchanges/%2f/amq.default/publish```

```curl -u guest:guest -X POST -H "Content-Type: application/json" -d '{"properties":{},"routing_key":"input_queue","payload":"[\"107\", \"Netflix расширяет библиотеку собственных сериалов.\", \"Netflix\"]","payload_encoding":"string"}' http://localhost:15672/api/exchanges/%2f/amq.default/publish```

```curl -u guest:guest -X POST -H "Content-Type: application/json" -d '{"properties":{},"routing_key":"input_queue","payload":"[\"108\", \"IBM представила новые решения для облачных вычислений.\", \"IBM\"]","payload_encoding":"string"}' http://localhost:15672/api/exchanges/%2f/amq.default/publish```

```curl -u guest:guest -X POST -H "Content-Type: application/json" -d '{"properties":{},"routing_key":"input_queue","payload":"[\"109\", \"Samsung запускает производство новых чипов.\", \"Samsung\"]","payload_encoding":"string"}' http://localhost:15672/api/exchanges/%2f/amq.default/publish```

```curl -u guest:guest -X POST -H "Content-Type: application/json" -d '{"properties":{},"routing_key":"input_queue","payload":"[\"110\", \"Twitter (X) изменил правила модерации контента.\", \"Twitter\"]","payload_encoding":"string"}' http://localhost:15672/api/exchanges/%2f/amq.default/publish```

### Пример выхода
```astapi-container  | DEBUG:main:Получено новое сообщение: b'["101", "\xd0\xad\xd0\xbf\xd0\xbf\xd0\xbb \xd0\xbe\xd1\x82\xd0\xb2\xd1\x80\xd0\xb0\xd1\x82\xd0\xbd\xd1\x8b\xd0\xb5 \xd0\xbf\xd0\xb8\xd0\xb4\xd0\xb0\xd1\x80\xd0\xb0\xd1\x81\xd1\x8b \xd0\xbf\xd1\x80\xd0\xbe\xd1\x81\xd1\x82\xd0\xbe \xd0\xbd\xd0\xb0\xd0\xb6\xd1\x80\xd0\xb0\xd0\xbb\xd0\xb8\xd1\x81\xd1\x8c \xd1\x85\xd1\x83\xd0\xb5\xd0\xb2 \xd0\xb0\xd0\xb9\xd1\x84\xd0\xbe\xd0\xbd \xd1\x85\xd1\x83\xd0\xb5\xd1\x82\xd0\xb0 \xd1\x81\xd0\xbe\xd0\xb1\xd0\xb0\xd1\x87\xd1\x8c\xd1\x8f", "Apple"]'
fastapi-container  | DEBUG:main:Сообщение раскодировано: ['101', 'Эппл отвратные пидарасы просто нажрались хуев айфон хуета собачья', 'Apple']
fastapi-container  | DEBUG:main:Обработка новости 101 для компании Apple
fastapi-container  | DEBUG:main:Отправляем запрос к OpenAI. news_id=101, company=Apple                                                                
fastapi-container  | DEBUG:main:Загрузка системного промпта...                                                                                        
fastapi-container  | INFO:main:Системный промпт успешно загружен.                                                                                     
fastapi-container  | DEBUG:main:Отправляем запрос в OpenAI chat.completions.acreate                                                                   
fastapi-container  | DEBUG:openai._base_client:Request options: {'method': 'post', 'url': '/chat/completions', 'files': None, 'json_data': {'messages': [{'role': 'system', 'content': 'Ты помощник, который анализирует новости. Тебе даются текст новости и компания. Определи сентимент упоминания компании в новости: только одно слово из списка ["Positive","Neutral","Negative"].'}, {'role': 'user', 'content': 'Новость:\nЭппл отвратные пидарасы просто нажрались хуев айфон хуета собачья\n\nКомпания: Apple\nВыведи строго один вариант: Positive или Neutral или Negative.'}], 'model': 'gpt-4o'}}
fastapi-container  | DEBUG:httpcore.connection:close.started
fastapi-container  | DEBUG:httpcore.connection:close.complete
fastapi-container  | DEBUG:httpcore.connection:connect_tcp.started host='api.openai.com' port=443 local_address=None timeout=5.0 socket_options=None  
fastapi-container  | DEBUG:httpcore.connection:connect_tcp.complete return_value=<httpcore._backends.anyio.AnyIOStream object at 0x7f4cd95cb190>      
fastapi-container  | DEBUG:httpcore.connection:start_tls.started ssl_context=<ssl.SSLContext object at 0x7f4cd9fd41c0> server_hostname='api.openai.com' timeout=5.0                                                                                                                                         
fastapi-container  | DEBUG:httpcore.connection:start_tls.complete return_value=<httpcore._backends.anyio.AnyIOStream object at 0x7f4cd9685070>
fastapi-container  | DEBUG:httpcore.http11:send_request_headers.started request=<Request [b'POST']>
fastapi-container  | DEBUG:httpcore.http11:send_request_headers.complete                                                                              
fastapi-container  | DEBUG:httpcore.http11:send_request_body.started request=<Request [b'POST']>                                                      
fastapi-container  | DEBUG:httpcore.http11:send_request_body.complete                                                                                 
fastapi-container  | DEBUG:httpcore.http11:receive_response_headers.started request=<Request [b'POST']>                                               
fastapi-container  | DEBUG:aiormq.connection:Prepare to send ChannelFrame(payload=b'\x08\x00\x00\x00\x00\x00\x00\xce', should_close=False, drain_future=None)                                                                                                                                               
fastapi-container  | DEBUG:httpcore.http11:receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Fri, 13 Dec 2024 14:37:33 GMT'), (b'Content-Type', b'application/json'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'), (b'access-control-expose-headers', b'X-Request-ID'), (b'openai-organization', b'user-ndo6pwbhi0g17ywuwy2acxyo'), (b'openai-processing-ms', b'370'), (b'openai-version', b'2020-10-01'), (b'x-ratelimit-limit-requests', b'500'), (b'x-ratelimit-limit-tokens', b'30000'), (b'x-ratelimit-remaining-requests', b'499'), (b'x-ratelimit-remaining-tokens', b'29837'), (b'x-ratelimit-reset-requests', b'120ms'), (b'x-ratelimit-reset-tokens', b'326ms'), (b'x-request-id', b'req_335bd3aff27ff90ebfc97077d0acf637'), (b'strict-transport-security', b'max-age=31536000; includeSubDomains; preload'), (b'CF-Cache-Status', b'DYNAMIC'), (b'X-Content-Type-Options', b'nosniff'), (b'Server', b'cloudflare'), (b'CF-RAY', b'8f16b1593dc9fff2-AMS'), (b'Content-Encoding', b'gzip'), (b'alt-svc', b'h3=":443"; ma=86400')])
fastapi-container  | INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
fastapi-container  | DEBUG:httpcore.http11:receive_response_body.started request=<Request [b'POST']>                                                  
fastapi-container  | DEBUG:httpcore.http11:receive_response_body.complete                                                                             
fastapi-container  | DEBUG:httpcore.http11:response_closed.started
fastapi-container  | DEBUG:httpcore.http11:response_closed.complete                                                                                   
fastapi-container  | DEBUG:openai._base_client:HTTP Request: POST https://api.openai.com/v1/chat/completions "200 OK"
fastapi-container  | DEBUG:main:Ответ от OpenAI получен: ChatCompletion(id='chatcmpl-Ae15J0bpGcfFk3VG1x29id6XGb8YR', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='Negative', refusal=None, role='assistant', audio=None, function_call=None, tool_calls=None))], created=1734100653, model='gpt-4o-2024-08-06', object='chat.completion', service_tier=None, system_fingerprint='fp_9faba9f038', usage=CompletionUsage(completion_tokens=1, prompt_tokens=99, total_tokens=100, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))       
fastapi-container  | DEBUG:main:OpenAI вернул: Negative
fastapi-container  | INFO:main:Определён сентимент: Negative для новости 101                                                                          
fastapi-container  | DEBUG:main:Отправляем результат в выходную очередь: ['101', 'Negative']                                                          
fastapi-container  | DEBUG:aio_pika.exchange:Publishing message with routing key 'output_queue' via exchange <RobustExchange(): auto_delete=False, durable=False, arguments={})>: Message:{'app_id': None,                                                                                                  
fastapi-container  |  'body_size': 19,
fastapi-container  |  'cluster_id': None,
fastapi-container  |  'consumer_tag': None,                                                                                                           
fastapi-container  |  'content_encoding': None,                                                                                                       
fastapi-container  |  'content_type': None,                                                                                                           
fastapi-container  |  'correlation_id': None,                                                                                                         
fastapi-container  |  'delivery_mode': <DeliveryMode.NOT_PERSISTENT: 1>,                                                                              
fastapi-container  |  'delivery_tag': None,                                                                                                           
fastapi-container  |  'exchange': None,                                                                                                               
fastapi-container  |  'expiration': None,
fastapi-container  |  'headers': {},                                                                                                                  
fastapi-container  |  'message_id': None,                                                                                                             
fastapi-container  |  'priority': 0,
fastapi-container  |  'redelivered': None,                                                                                                            
fastapi-container  |  'reply_to': None,                                                                                                               
fastapi-container  |  'routing_key': None,
fastapi-container  |  'timestamp': None,                                                                                                              
fastapi-container  |  'type': 'None',                                                                                                                 
fastapi-container  |  'user_id': None}                                                                                                                
fastapi-container  | DEBUG:aiormq.connection:Prepare to send ChannelFrame(payload=b'\x01\x00\x01\x00\x00\x00\x15\x00<\x00(\x00\x00\x00\x0coutput_queue\x01\xce\x02\x00\x01\x00\x00\x005\x00<\x00\x00\x00\x00\x00\x00\x00\x00\x00\x138\x80\x00\x00\x00\x00\x01\x00 ecc64f79110f45669b06a97bf281880e\xce\x03\x00\x01\x00\x00\x00\x13["101", "Negative"]\xce', should_close=False, drain_future=<Future pending cb=[FutureStore.__on_task_done.<locals>.remover() at /usr/local/lib/python3.9/site-packages/aiormq/base.py:33, <1 more>, <TaskWakeupMethWrapper object at 0x7f4cd95de850>()]>)
fastapi-container  | DEBUG:aiormq.connection:Received frame <Basic.Ack object at 0x7f4cd95df100> in channel #1 weight=21 on <Connection: "amqp://guest:******@rabbitmq:5672/" at 0x7f4cd9f3a4f0>                                                                                                            
fastapi-container  | INFO:main:Результат отправлен в output_queue: ['101', 'Negative']
fastapi-container  | DEBUG:aiormq.connection:Prepare to send ChannelFrame(payload=b'\x01\x00\x01\x00\x00\x00\r\x00<\x00P\x00\x00\x00\x00\x00\x00\x00\x02\x00\xce', should_close=False, drain_future=<Future pending cb=[FutureStore.__on_task_done.<locals>.remover() at /usr/local/lib/python3.9/site-packages/aiormq/base.py:33, <1 more>, <TaskWakeupMethWrapper object at 0x7f4cd9ee0dc0>()]>)
Gracefully stopping... (press Ctrl+C again to force)```
