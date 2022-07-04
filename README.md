# SynTERRA
Web app for exploring the database of text-mined synthesis "recipes"

### Version 1.0.0

### Running local version

1. Install [MatQuery] (https://github.com/CederGroupHub/MatQuery) - private repository of CEDER Group
2. Setup variables to connect to the synthesis database: `PRO_MONGO_HOST`, `PRO_MONGO_PORT`, `PRO_MONGO_DB`, `PRO_MONGO_USER`, `PRO_MONGO_PASSWD`
3. Run MatQuery API: `uvicorn matquery_api:app --host=HOST_NAME --port=PORT_NUMBER --reload`
4. Set variable `MATQUERY_API` to `http://HOST_NAME+PORT_NUMBER`
5. Run `python app.py` or `uvicorn app:app --host=ANOTHER_HOST_NAME --port=ANOTHER_PORT_NUMBER`



