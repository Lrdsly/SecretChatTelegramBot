from db.pool import execute, fetchone

# ---- ENJOY CODING TODAY ----

async def end_connection(user_id, against_id):
    query = """UPDATE a_connections SET closed_at=NOW() WHERE 
             user1_id = %s
             AND user2_id = %s 
             AND closed_at IS NULL"""
    await execute(query, (user_id, against_id))
    await execute(query, (against_id, user_id))

async def create_a_connections_row(user1_id:int, user2_id:int):
    query = "INSERT INTO a_connections (user1_id, user2_id) VALUES (%s, %s)"
    await execute(query, (user1_id, user2_id))

async def verify_a_connection(user_id:int):
    check1 = """SELECT EXISTS (
             SELECT 1 FROM a_connections WHERE
             (user1_id = %s OR user2_id = %s)
             AND closed_at IS NULL)
             """
    check2 = """SELECT EXISTS (
             SELECT 1 FROM sa_connections WHERE
             (user_id = %s)
             AND closed_at IS NULL)
             """
    r1 = await fetchone(check1, (user_id, user_id))
    r2 = await fetchone(check2, (user_id,))
    return not (r1[0] or r2[0])
