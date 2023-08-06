# Supabase
import decouple
from supabase import create_client, Client

# Get your project URL and API key from the Supabase dashboard
url:str = decouple.config("SUPABASE_MRDATA_PROJECT_URL")
key:str = decouple.config("SUPABASE_MRDATA_API_KEY")
email:str = decouple.config("SUPABASE_USER")
password:str = decouple.config("SUPABASE_PASSWORD")
mr_db:Client = create_client(url, key)
user = mr_db.auth.sign_in_with_password({ "email": email, "password": password })

# user=postgres
# password=[YOUR-PASSWORD]
# host=db.cahulnvuzydcxbjzxnxc.supabase.co
# port=5432
# database=postgres