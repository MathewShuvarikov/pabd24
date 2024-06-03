# Report
Research of the behavior of flask and gunicorn servers under different types of load. 

### Research method

In the file `src/utils.py `three functions have been defined that emulate three solutions to the `predict` problem :
- `predict_io_bounded(area)` - corresponds to the second option, a request to a third-party service replaces `time.sleep(1)'. 
This corresponds to a delay of 1 second, which is needed to exchange information with a third-party service. 
At the same time, the computational load on our server is not created, the process simply sleeps. 
- `predict_cpu_bounded(area, n)` - corresponds to the first variant, the predicate on its own server. 
The `n` parameter allows you to adjust the load, in fact it is just calculating the arithmetic mean of a linear array. 
If the `n` is large enough, the server will issue an error due to lack of memory. 
It is necessary to determine this value empirically. 
- `predict_cpu_multithread(area, n)' - also corresponds to the first option, but optimized numpy code is used. 
It is also necessary to empirically determine the critical value of `n` and compare it with the previous one. 

There are two options available to launch the service: 
- `python src/predict_app.py ` is a server designed for development. 
- `gunicorn src.predict_app:app` is a server designed for continuous operation in production. 

The load is created by the file `test/test_parallel.py `.  


### Results and discussion
1) При запуске predict_cpu_multithread на dev-сервере flask с n=20_000_000 получен [результат](log/test_np_flask.txt). 
Все запросы обрабатываются одновременно, в среднем за 20 секунды. 
На продакшене это неприемлимо, потому что ... 

2) При запуске predict_cpu_multithread на prod-сервере gunicorn с n=20_000_000 получен [результат](log/test_np_flask.txt). 
Все запросы обрабатываются последовательно, в среднем за 20 секунды. 
На продакшене это предпочтительно, потому что ... 

...

6)
