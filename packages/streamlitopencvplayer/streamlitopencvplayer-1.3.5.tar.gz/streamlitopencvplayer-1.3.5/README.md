Streamlit Opencv Player is a video player written in python for easy video playback and frames management using OpenCV

### Prerequisites
- Python 3.8
- Conda

### Create conda environnement
You should have already installed `Anaconda`.
Verify that conda is installed and running on your system by typing:
```
conda --version
```
1. Create a new environment : 
    ```
    conda create --name myenv
    ```
2. Activate the new environment :
    ```
    conda activate myenv
    ```
### Install libraries:
   
   ```
   pip install -r requirements.txt
   ```



### Run Test script 

* Run the app:
    ```
    streamlit run test/test.py -- -V "video path or url"
    ```
