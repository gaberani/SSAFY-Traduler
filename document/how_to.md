# How_To_Run

## First

* install Node.js / NPM / Python 3.6

* Clone Repository

    ```bash
    git clone https://lab.ssafy.com/s03-final/s03p31a505.git
    
    cd s03p31a505
    ```

    

## Run front-end

* Build front-end environment

    ```bash
    cd frontend
    npm install
    ```

* make local env file (`.env.local`)

    ```
    VUE_APP_DH_SERVER_URL = {User DH SERVER URL}
    VUE_APP_KU_SERVER_URL = {User KU SERVER URL}
    VUE_APP_SERVER_URL = {User SERVER URL}
    VUE_APP_KAKAO_MAP_JS_KEY = {KAKAO MAP JS KEY}
    ```

* run front-end server

    ```bash
    npm run serve
    ```

    

## Run back-end

* Build environment

    ```bash
    cd backend
    python -m venv tradulerenv
    source tradulerenv/Scripts/activate
    pip install -r requirements.txt
    ```

* make local env file (`db_settings.py` in `traduler` folder)

    ```
    DATABASES = {
        'default' : {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': { DB NAME },
            'USER': { DB User NAME },
            'PASSWORD': { DB Password },
            'HOST': { DB SERVER URL },
            'PORT': { DB PORT },
        }
    }
    ```

* run back-end server

    ```bash
    python manage.py runserver
    ```

    