
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from db.redis import *
import pytest

# ---- Life is good, not best, but good ----

@pytest.mark.asyncio
async def test_user_state_managment():
    # delete past status
    await r.delete("state:1111")
    await r.delete("state:2222")
    await r.delete("state:3333")
    
    await update_user_state(1111, "searching")
    await update_user_state(2222, "anon-chat")
    await update_user_state(3333, "semi-chat")    

    user1 = await get_user_state(1111)
    user2 = await get_user_state(2222)
    user3 = await get_user_state(3333)
    
    assert user1 == "searching"
    assert user2 == "anon-chat"
    assert user3 == "semi-chat"