FROM python:3.9.13

COPY salient_point.py .			
COPY schemes.py .	
#Bpm Heart Rate Path		
COPY all_bpm.p .
COPY main.py . 
COPY analysis.py .			
RUN pip install numpy
CMD ["python", "./main.py"]