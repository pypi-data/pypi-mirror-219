import sys
import os
import pytest
import dotenv 



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db')))
from library import Accsess_Token_Library


dotenv.load_dotenv()

@pytest.mark.test
def test_getProfiles_returns_name_and_email():
    insert1 = Accsess_Token_Library()
    insert1.insert_user_external("test",2,"test1")

    token=insert1.get_access_token_by_user_name("test")
    assert token[0]=="test1"


    

    
