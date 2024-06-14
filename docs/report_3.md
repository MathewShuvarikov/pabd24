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
* We have used the second one

The load is created by the file `test/test_parallel.py `.  


### Results and discussion
1) When running predict_io_bounded on the gunicorn prom server we obtained [result](https://github.com/MathewShuvarikov/pabd24/blob/main/log/test_gunicorn_predict_io_bounded.txt). 
All requests are processed sequentially, in an average of 5.6 seconds.

2) When running predict_cpu_bounded on the gunicorn prom server with n=15_000_000, we obtained [result](https://github.com/MathewShuvarikov/pabd24/blob/main/log/test_gunicorn_cpu_15mln.txt). 
All requests are processed sequentially, in an average of 5.7 seconds. Server collapses with n = 17_500_000.

3) When running predict_cpu_multithread on the gunicorn prom server with n=75_000_000, we obtained [result](https://github.com/MathewShuvarikov/pabd24/blob/main/log/test_gunicorn_mult_75mln.txt). 
All requests are processed sequentially, in an average of 2.5 seconds. Server collapses with n = 90_000_000.

4) When running predict_io_bounded on the flask dev server , we obtained [result](https://github.com/MathewShuvarikov/pabd24/blob/main/log/test_flask_predict_io_bounded.txt). 
All requests are processed simultaneously, in an average of 0.08 seconds.

5) When running predict_cpu_bounded on the flask dev server with n=15_000_000, we obtained [result](https://github.com/MathewShuvarikov/pabd24/blob/main/log/test_flask_predict_cpu_bounded.txt). 
All requests are processed simultaneously, in an average of 0.08 seconds.

6) When running predict_cpu_multithread on the flask dev server with n=75_000_000, we obtained [result](https://github.com/MathewShuvarikov/pabd24/blob/main/log/test_flask_predict_mult_bounded.txt). 
All requests are processed simultaneously, in an average of 0.07 seconds.


### Conclusion
Based on the test results, the following conclusions can be drawn:
- Flask is suitable for development and testing, but it does not suit the high workload in production.
- Gunicorn shows the best results under heavy load.