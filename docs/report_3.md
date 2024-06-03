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
1) When running predict_cpu_bounded on the flask dev server with n=5_000_000, we obtained [result](https://github.com/MathewShuvarikov/pabd24/blob/main/log/test_np_flask_cpu_5mln.txt). 
All requests are processed simultaneously, in an average of 2 seconds. 
In production, this is acceptable since it is a comparably fast result.

2) When running predict_cpu_bounded on the flask dev server with n=15_000_000, we obtained [result](https://github.com/MathewShuvarikov/pabd24/blob/main/log/test_np_flask_cpu_15mln.txt). 
All requests are processed simultaneously, in an average of 5.7 seconds. 
In production, it's worse than the previous result, an average user won't appreciate such a long answer.

2) When running predict_cpu_bounded on the flask dev server with n=17_500_000, we obtained [result](log/test_np_flask_cpu_17_5mln.txt). 
Server collapses. It is out of memory.

4) When running predict_cpu_multithread on the flask dev server with n=75_000_000, we obtained [result](log/test_np_flask_mult_75mln.txt). 
All requests are processed simultaneously, in an average of 2.5 seconds. 
In production, this is acceptable since it is a comparably fast result.

5) When running predict_cpu_multithread on the flask dev server with n=80_000_000, we obtained [result](log/test_np_flask_mult_80mln.txt). 
All requests are processed simultaneously, in an average of 3.1 seconds.

6) When running predict_cpu_multithread on the flask dev server with n=90_000_000, we obtained [result](log/test_np_flask_mult_90mln.txt). 
Server collapses. It is out of memory.