1. Create a virtual environment by using the following command:
    * for windows
        ```
        python -m venv env
        ```
    * for mac
        ```
        python3 -m venv env
        ```
    
2. Next you need to activate the virtual environment as:
    * for windows
        ```
        env\Scripts\activate
        ```
    * for mac
        ```
        source env/bin/activate
        ```

3. Clone the repository using the following command:
    ```
    git clone https://github.com/tkarotra/ChatApp.git
    ```

4. We  now need to move into our project folder. Do this by running the following command:
    ```
    cd ChatApp
    ```

5. Now we need to install all the dependencies of the project. This can be done using the following command:
    ```
    pip install -r requirements.txt
    ```

6. Next you need to run the following command to setup our database:
    ```
    python manage.py makemigrations
    ```
    or
    ```
    python manage.py makemigrations app
    ```

7. Then we simply need to apply these migrations by running:
    ```
    python manage.py migrate
    ```

8. Next we need to create a super user to acess the database and all its tables:
    ```
    python manage.py createsuperuser
    ```

9. Now finally to run the development server as follows:
    ```
    python manage.py runserver
    ```

## Now you have setup the project successfully!!


> NOTE : You can refer the below table for the shortcuts to all the commands that were used above and more.
>
>> Just remeber to run `pip install django-shortcuts` command to use the bellow shortcuts.

<br />

|Original Command|Shortcut|
|:---|:---|
|```python manage.py runserver```|```django r```|
|```python manage.py makemigrations```|```django mm```|
|```python manage.py migrate```|```django m```|
|```python manage.py createsuperuser```|```django csu```|
|```python manage.py collectstatic```|```django c```|
|```python manage.py shell```|```django s```|
|```python manage.py changepassword```|```django cpw```|
