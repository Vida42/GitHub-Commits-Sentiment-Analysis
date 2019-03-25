import sqlite3 as sqlite
import senti_calculator

with sqlite.connect('./whole_database_new.db') as con:    
    cur = con.cursor() # get the current spot for executing        
    cur.execute("SELECT * FROM commit_sentiments")
    rows = cur.fetchall()

    for row in rows:
        ccid = row[0]
        body = row[1]
        # print(body)
        # print(type(body))
        created_at = row[2]
        sha = row[3]
        project_name = row[4]
        language = row[5]
        email = row[6]
        login = row[7]
        loc = row[8]
        pos = row[9]
        neg = row[10]

        com = senti_calculator.myVader(body)

        with sqlite.connect('./vader_databse.db') as con:
            con.text_factory = str
            cur = con.cursor() # get the current spot for executing
            cur.execute("""INSERT INTO commit_sentiments_store 
                (commit_comment_id,
                 commit_comment_body,
                 sentiment_com)
                 VALUES (?, ?, ?)""", 
                (ccid, body, com)) # execute insert to add the score and name
            con.commit() # commit the query

        with sqlite.connect('./vader_databse.db') as con:
            con.text_factory = str
            cur = con.cursor() # get the current spot for executing
            cur.execute("""INSERT INTO commit_sentiments
                (commit_comment_id, 
                 commit_comment_body,
                 created_at,
                 commit_sha,
                 project_name,
                 project_language,
                 commenter_email,
                 commenter_login,
                 location,
                 sentiment_pos, 
                 sentiment_neg,
                 sentiment_com)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                (ccid, body, created_at, sha, project_name, language, email, login, loc, pos, neg, com)) # execute insert to add the score and name
            con.commit() # commit the query