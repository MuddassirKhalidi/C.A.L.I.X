from memory import VectorStore
from aida import AIDA
from dotenv import load_dotenv
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

load_dotenv(dotenv_path=os.path.join('refactoring', '.env'))
store = VectorStore()
aida = AIDA(store)
# aida.get_conversation()
query = aida.get_query()
aida.generate_response(query)